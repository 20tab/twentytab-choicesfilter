twentytab-choicesfilter
=======================

A django app that initializes admin changelist view with select filters usin jquery-plugin select2

## Installation

Use the following command: <b><i>pip install twentytab-choicesfilter</i></b>

## Configuration

- settings.py

```py
INSTALLED_APPS = {
    ...,
    'select2',
    'choicesfilter',
    ...
}
```


- Static files

Run collectstatic command or map static directory. If you use uWSGI you can map static files:

```ini
static-map = /static/select2/=%(path_to_site_packages)/select2/static/select2
static-map = /static/choicesfilter/=%(path_to_site_packages)/choicesfilter/static/choicesfilter
```

## Usage

- models.py

```py

class MyModel(models.Model):
    name = models.CharField(...)
    related_obj = models.ForeignKey(MyRelated)

```

- admin.py

```py
from django.contrib import admin
from mymodels.models import MyModel
from choicesfilter.admin import ChoicesFilterAdmin


class MyModelAdmin(ChoicesFilterAdmin):
    list_display = (u'nome', u'related_obj')
    choicesfilter = [u'nome', 'related_obj']
    choices_mandatory = False

admin.site.register(MyModel, MyModelAdmin)
```

If you want to initialize changelist admin view with empty queryset set 'choices_mandatory = True'
