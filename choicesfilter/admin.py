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
            self.fields[k].label = l.split('__')[-1].title()
            self.fields[k].widget = SelectAutocomplete(plugin_options={"width": "300px"}, choices=v.choices)


class ChoicesFilterAdmin(admin.ModelAdmin):
    change_list_template = u'choicesfilter.html'
    choicesfilter = []
    choices_mandatory = False
    choicesfilter_choices = {}
    related_choicesfilter = []

    def _get_recursive_related_choices(self, model, fields_as_list):
        if len(fields_as_list) < 1:
            return None
        elif len(fields_as_list) == 1:
            f = fields_as_list[0]
            field = model._meta.get_field(f)
            if field.__class__.__name__ == u'ForeignKey':
                if f in self.choicesfilter_choices.keys():
                    choices = self.choicesfilter_choices[f]
                else:
                    choices = [(u'', u'---------')]
                    choices.extend([(el.pk, el.__unicode__()) for el in field.related.parent_model.objects.filter(
                        **field.rel.limit_choices_to
                    )])
                return forms.ChoiceField(choices=choices, required=False)
        else:
            f = fields_as_list[0]
            field = model._meta.get_field(f)
            return self._get_recursive_related_choices(field.related.parent_model, fields_as_list[1:])

    def changelist_view(self, request, extra_context=None):
        if self.choicesfilter:
            extra_context = extra_context or {}

            temp_list = []
            for f in self.choicesfilter:
                field = self.model._meta.get_field(f)
                if field.__class__.__name__ == u'ForeignKey':
                    if f in self.choicesfilter_choices.keys():
                        choices = self.choicesfilter_choices[f]
                    else:
                        choices = [(u'', u'---------')]
                        choices.extend([(el.pk, el.__unicode__()) for el in field.related.parent_model.objects.filter(
                            **field.rel.limit_choices_to
                        )])
                    filter_field = forms.ChoiceField(choices=choices, required=False)
                    temp_list.append((f, u'{}__id__exact'.format(f), filter_field))
                elif field.__class__.__name__ == u'CharField' and getattr(field, u'choices', None):
                    if f in self.choicesfilter_choices.keys():
                        choices = self.choicesfilter_choices[f]
                    else:
                        choices = [(u'', u'---------')]
                        choices.extend(list(field.choices))
                    filter_field = forms.ChoiceField(choices=choices, required=False)
                    temp_list.append((f, u'{}__icontains'.format(f), filter_field))
                else:
                    raise ImproperlyConfigured(
                        u'The field \'{}\' is not a ForeignKey or it hasn\'t choices parameter!'.format(f)
                    )

            for f in self.related_choicesfilter:
                filter_field = self._get_recursive_related_choices(self.model, f.split(u'__'))
                if filter_field:
                    temp_list.append((f, u'{}__id__exact'.format(f), filter_field))

                # field = self.model._meta.get_field(f)
                # if field.__class__.__name__ == u'ForeignKey':
                #     if f in self.choicesfilter_choices.keys():
                #         choices = self.choicesfilter_choices[f]
                #     else:
                #         choices = [(u'', u'---------')]
                #         choices.extend([(el.pk, el.__unicode__()) for el in field.related.parent_model.objects.filter(
                #             **field.rel.limit_choices_to
                #         )])
                #     filter_field = forms.ChoiceField(choices=choices, required=False)
                #     temp_list.append((f, u'{}__id__exact'.format(f), filter_field))

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
