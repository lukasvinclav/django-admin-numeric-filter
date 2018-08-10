from django.contrib import admin
from django.contrib.admin.utils import reverse_field_path
from django.db.models import Min, Max

from .forms import RangeNumericForm, SingleNumericForm, SliderNumericForm


class SingleNumericFilter(admin.FieldListFilter):
    parameter_name = None
    template = 'admin/filter_numeric_single.html'

    def __init__(self, field, request, params, model, model_admin, field_path):        
        super().__init__(field, request, params, model, model_admin, field_path)
        
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
            'form': SingleNumericForm(name=self.parameter_name, data={self.parameter_name: self.value()}),
        }, )


class RangeNumericFilter(admin.FieldListFilter):
    parameter_name = None
    template = 'admin/filter_numeric_range.html'

    def __init__(self, field, request, params, model, model_admin, field_path):        
        super().__init__(field, request, params, model, model_admin, field_path)
        
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
        
        if self.used_parameters.get(self.parameter_name + '_from', None) is not None:
            filters.update({
                self.parameter_name + '__gte': self.used_parameters.get(self.parameter_name + '_from', None),
            })

        if self.used_parameters.get(self.parameter_name + '_to', None) is not None:
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
            'form': RangeNumericForm(name=self.parameter_name, data={
                self.parameter_name + '_from': self.used_parameters.get(self.parameter_name + '_from', None),
                self.parameter_name + '_to': self.used_parameters.get(self.parameter_name + '_to', None),
            }),
        }, )


class SliderNumericFilter(RangeNumericFilter):
    template = 'admin/filter_numeric_slider.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        parent_model, reverse_path = reverse_field_path(model, field_path)

        if model == parent_model:
            self.q = model_admin.get_queryset(request)
        else:
            self.q = parent_model._default_manager.all()

    def choices(self, changelist):
        min = self.q.all().aggregate(min=Min(self.parameter_name)).get('min', 0)
        max = self.q.all().aggregate(max=Max(self.parameter_name)).get('max', 0)

        return ({
            'min': min,
            'max': max,
            'value_from': self.used_parameters.get(self.parameter_name + '_from', min),
            'value_to': self.used_parameters.get(self.parameter_name + '_to', max),
            'form': SliderNumericForm(name=self.parameter_name, data={
                self.parameter_name + '_from': self.used_parameters.get(self.parameter_name + '_from', min),
                self.parameter_name + '_to': self.used_parameters.get(self.parameter_name + '_to', max),
            })
        }, )
