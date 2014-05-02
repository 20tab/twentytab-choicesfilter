from django.contrib import admin
from select2.widgets import SelectAutocomplete
from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class ChoicesFilterForm(forms.Form):
    def __init__(self, choicesfilter, *args, **kwargs):
        super(ChoicesFilterForm, self).__init__(*args, **kwargs)
        for (l, k, v) in choicesfilter:
            self.fields[k] = v
            self.fields[k].label = l.title()
            self.fields[k].widget = SelectAutocomplete(plugin_options={"width": "300px"}, choices=v.choices)


class ChoicesFilterAdmin(admin.ModelAdmin):
    change_list_template = u'choicesfilter.html'
    choicesfilter = []
    choices_mandatory = False

    def changelist_view(self, request, extra_context=None):
        if self.choicesfilter:
            extra_context = extra_context or {}

            temp_list = []
            for f in self.choicesfilter:
                field = self.model._meta.get_field(f)
                if field.__class__.__name__ == u'ForeignKey':
                    choices = [(u'', u'---------')]
                    choices.extend([(el.pk, el.__unicode__()) for el in field.related.parent_model.objects.filter(
                        **field.rel.limit_choices_to
                    )])
                    filter_field = forms.ChoiceField(choices=choices, required=False)
                    temp_list.append((f, u'{}__id__exact'.format(f), filter_field))
                elif field.__class__.__name__ == u'CharField' and getattr(field, u'choices', None):
                    choices = [(u'', u'---------')]
                    choices.extend(list(field.choices))
                    filter_field = forms.ChoiceField(choices=choices, required=False)
                    temp_list.append((f, u'{}__icontains'.format(f), filter_field))
                else:
                    raise ImproperlyConfigured(
                        u'The field \'{}\' is not a ForeignKey or it hasn\'t choices parameter!'.format(f)
                    )

            extra_context['choicesfilter'] = ChoicesFilterForm(temp_list, request.GET)
        return super(ChoicesFilterAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super(ChoicesFilterAdmin, self).get_queryset(request)
        if self.choices_mandatory and not request.GET:
            return qs.none()
        return qs

    class Media:
        js = SelectAutocomplete.Media.js + (u'{}choicesfilter/js/choicesfilter.js'.format(settings.STATIC_URL),)
        css = SelectAutocomplete.Media.css
