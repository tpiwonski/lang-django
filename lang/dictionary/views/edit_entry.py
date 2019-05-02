from django import forms
from django.views.generic.base import View
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import redirect

from lang.dictionary.db.entry import LANGUAGES
from lang.common.component import ComponentContext, ComponentView
from lang.dictionary.controllers import GetEntry, EditEntry
from lang.dictionary.views.base import BaseContext


class EntryForm(forms.Form):
    id = forms.UUIDField(widget=forms.HiddenInput())
    text = forms.CharField(max_length=255)
    language = forms.ChoiceField(choices=LANGUAGES)


class TranslationForm(forms.Form):
    id = forms.UUIDField(required=False, widget=forms.HiddenInput())
    text = forms.CharField(required=True)
    language = forms.ChoiceField(choices=LANGUAGES)


class TranslationFormSet(forms.BaseFormSet):

    def clean(self):
        for form in self.forms:
            if not form.cleaned_data.get('text'):
                form.add_error('text', u'Field cannot be empty')


TranslationFormSet = forms.formset_factory(TranslationForm, formset=TranslationFormSet, extra=0, can_delete=True)


class EditEntryView(ComponentView):
    template_name = 'dictionary/pages/edit_entry.html'
    get_entry_controller = GetEntry()
    edit_entry_controller = EditEntry()
    context_classes = [BaseContext]

    def get_context_data(self, entry_id, **kwargs):
        context = super().get_context_data(**kwargs)

        entry = self.get_entry_controller.execute(entry_id)
        context.update({
            'entry': entry,
            'entry_form': EntryForm(entry),
            'translation_forms': TranslationFormSet(initial=entry['translations'])
        })
        return context

    def post(self, request, entry_id, *args, **kwargs):
        entry = self.get_entry_controller.execute(entry_id)
        entry_form = EntryForm(request.POST)
        translation_forms = TranslationFormSet(request.POST, initial=entry['translations'])
        valid_entry = entry_form.is_valid()
        valid_translations = translation_forms.is_valid()
        if not valid_entry or not valid_translations:
            context = super().get_context_data(**kwargs)
            context.update({
                'entry': entry,
                'entry_form': entry_form,
                'translation_forms': translation_forms
            })
            return self.render_to_response(context)

        self.edit_entry_controller.execute(entry_form.cleaned_data, translation_forms.cleaned_data)

        return redirect('entry-view', entry_id=entry['id'])
