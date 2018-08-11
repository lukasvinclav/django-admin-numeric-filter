# django-admin-numeric-filter

## Getting started

1. Install package directly from GitHub

```bash
pip install git+https://git@github.com/lukasvinclav/django-admin-numeric-filter.git
```

2. Add **admin_numeric_filter** into **INSTALLED_APPS** in your setting file

## Sample admin configuration

```python
from django.contrib import admin

from admin_numeric_filter.admin import SingleNumericFilter, RangeNumericFilter, SliderNumericFilter

from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_filter = (
        ('field_A', SingleNumericFilter), # Single field search, **gte** lookup
        ('field_B', RangeNumericFilter), # Range search, **gte** and **lte** lookup
        ('field_C', SliderNumericFilter), # Same as range above but with slider
    )
```