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

Run collectstatic command or map static directory.

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
    list_display = (u'name', u'related_obj')
    choicesfilter = [u'name', 'related_obj']
    choices_mandatory = False
    choicesfilter_choices = {'related_obj': RelatedClass.objects.values_list('pk', 'obj_field').all()}

admin.site.register(MyModel, MyModelAdmin)
```

If you want to initialize changelist admin view with empty queryset set 'choices_mandatory = True'

** REMEMBER: choicesfilter_choices MUST be a list of binary tuples like choices for a CharField **

** This app overrides {% block filters %} in change_list.html template. **
