![Screenshot](https://github.com/lukasvinclav/django-admin-numeric-filter/raw/master/screenshot.png)

# django-admin-numeric-filter

![](https://img.shields.io/badge/Version-0.1.2-orange.svg?style=flat-square)
![](https://img.shields.io/badge/Django-2.0+-green.svg?style=flat-square)
![](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)

django-admin-numeric-filter provides you several filter classes for Django admin which you can use to filter results in change list. It works in **list_filter** when a field name is defined as list where the first value is field name and second one is custom filter class (you can find classes below).

Don't forget to inherit your model admin from **admin_actions.admin.NumericFilterModelAdmin** to load custom CSS styles and JavaScript files declared in inner Media class.

## Getting started

1. Installation

```bash
pip install django-admin-numeric-filter
```

2. Add **admin_numeric_filter** into **INSTALLED_APPS** in your settings file before **django.contrib.admin**.

## Sample admin configuration

```python
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter

from .models import YourModel


class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 10


@admin.register(YourModel)
class YourModelAdmin(NumericFilterModelAdmin):
    list_filter = (
        ('field_A', SingleNumericFilter), # Single field search, __gte lookup
        ('field_B', RangeNumericFilter), # Range search, __gte and __lte lookup
        ('field_C', SliderNumericFilter), # Same as range above but with slider
        ('field_D', CustomSliderNumericFilter), # Filter with custom attributes
    )
```

## Filter classes

| Class name                               | Description                            |
|------------------------------------------|----------------------------------------|
| admin_actions.admin.SingleNumericFilter  | Single field search, __gte lookup      |
| admin_actions.admin.RangeNumericFilter   | Range search, __gte and __lte lookup   |
| admin_actions.admin.SliderNumericFilter  | Same as range above but with slider    |


## Slider default options for certain field types

| Django model field                       | Step                     | Decimal places             |
|------------------------------------------|--------------------------|----------------------------|
| django.db.models.fields.DecimalField()   | Based on decimal places  | max precision from DB      |
| django.db.models.fields.FloatField()     | Based on decimal places  | field decimal_places attr  |
| django.db.models.fields.IntegerField()   | 1                        | 0                          |