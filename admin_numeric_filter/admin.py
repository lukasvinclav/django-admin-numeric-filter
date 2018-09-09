from django.contrib import admin
from django.contrib.admin.utils import reverse_field_path
from django.db.models import Max, Min
from django.db.models.fields import DecimalField, FloatField, IntegerField

from .forms import RangeNumericForm, SingleNumericForm, SliderNumericForm


class NumericFilterModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (
                'js/nouislider.min.css',
                'css/admin-numeric-filter.css',
            )
        }
        js = (
            'js/wNumb.min.js',
            'js/nouislider.min.js',
            'js/admin-numeric-filter.js',
        )


class SingleNumericFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    template = 'admin/filter_numeric_single.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        if not isinstance(field, (DecimalField, IntegerField, FloatField)):
            raise TypeError('Class {} is not supported for {}.'.format(type(self.field), self.__class__.__name__))

        self.request = request

        if self.parameter_name is None:
            self.parameter_name = self.field.name

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})

    def value(self):
        return self.used_parameters.get(self.parameter_name, None)

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, changelist):
        return ({
            'request': self.request,
            'parameter_name': self.parameter_name,
            'form': SingleNumericForm(name=self.parameter_name, data={self.parameter_name: self.value()}),
        }, )


class RangeNumericFilter(admin.FieldListFilter):
    request = None
    parameter_name = None
    template = 'admin/filter_numeric_range.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        if not isinstance(field, (DecimalField, IntegerField, FloatField)):
            raise TypeError('Class {} is not supported for {}.'.format(type(self.field), self.__class__.__name__))

        self.request = request

        if self.parameter_name is None:
            self.parameter_name = self.field.name

        if self.parameter_name + '_from' in params:
            value = params.pop(self.parameter_name + '_from')
            self.used_parameters[self.parameter_name + '_from'] = value

        if self.parameter_name + '_to' in params:
            value = params.pop(self.parameter_name + '_to')
            self.used_parameters[self.parameter_name + '_to'] = value

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.parameter_name + '_from', None)
        if value_from is not None and value_from != '':
            filters.update({
                self.parameter_name + '__gte': self.used_parameters.get(self.parameter_name + '_from', None),
            })

        value_to = self.used_parameters.get(self.parameter_name + '_to', None)
        if value_to is not None and value_to != '':
            filters.update({
                self.parameter_name + '__lte': self.used_parameters.get(self.parameter_name + '_to', None),
            })

        return queryset.filter(**filters)

    def expected_parameters(self):
        return [
            '{}_from'.format(self.parameter_name),
            '{}_to'.format(self.parameter_name), 
        ]

    def choices(self, changelist):
        return ({
            'request': self.request,
            'parameter_name': self.parameter_name,
            'form': RangeNumericForm(name=self.parameter_name, data={
                self.parameter_name + '_from': self.used_parameters.get(self.parameter_name + '_from', None),
                self.parameter_name + '_to': self.used_parameters.get(self.parameter_name + '_to', None),
            }),
        }, )


class SliderNumericFilter(RangeNumericFilter):
    MAX_DECIMALS = 7
    MAX_STEP = 7

    template = 'admin/filter_numeric_slider.html'
    field = None


    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        self.field = field
        parent_model, reverse_path = reverse_field_path(model, field_path)

        if model == parent_model:
            self.q = model_admin.get_queryset(request)
        else:
            self.q = parent_model._default_manager.all()

    def choices(self, changelist):
        min_value = self.q.all().aggregate(min=Min(self.parameter_name)).get('min', 0)
        max_value = self.q.all().aggregate(max=Max(self.parameter_name)).get('max', 0)

        if isinstance(self.field, IntegerField):
            decimals = 0
            step = 1
        elif isinstance(self.field, FloatField):
            values = self.q.all().values_list(self.parameter_name, flat=True)
            max_precision = max(str(value)[::-1].find('.') for value in values)
            decimals = self._get_decimals(max_precision)
            step = self._get_min_step(max_precision)
        elif isinstance(self.field, DecimalField):
            step = self._get_min_step(self.field.decimal_places)
            decimals = self._get_decimals(self.field.decimal_places)

        return ({
            'decimals': decimals,
            'step': step,
            'parameter_name': self.parameter_name,
            'request': self.request,
            'min': min_value,
            'max': max_value,
            'value_from': self.used_parameters.get(self.parameter_name + '_from', min_value),
            'value_to': self.used_parameters.get(self.parameter_name + '_to', max_value),
            'form': SliderNumericForm(name=self.parameter_name, data={
                self.parameter_name + '_from': self.used_parameters.get(self.parameter_name + '_from', min_value),
                self.parameter_name + '_to': self.used_parameters.get(self.parameter_name + '_to', max_value),
            })
        }, )

    def _get_decimals(self, decimals):
        if decimals >= self.MAX_DECIMALS:
            return self.MAX_DECIMALS

        return decimals

    def _get_min_step(self, precision):
        result_format = '{{:.{}f}}'.format(precision - 1)
        return float(result_format.format(0) + '1')
