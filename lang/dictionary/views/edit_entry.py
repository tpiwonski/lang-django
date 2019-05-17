from django import forms
from django.shortcuts import redirect, render
from django.contrib import messages

from lang.common.component import ComponentView
from lang.dictionary.controllers import GetEntry, EditEntry
from lang.dictionary.db.entry import LANGUAGES
from lang.dictionary.views.base import BaseContext, PageView


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

    def get_translations_data(self):
        translations_data = []
        for form in self.forms:
            if form not in self.deleted_forms:
                translations_data.append(form.cleaned_data)
        
        return translations_data


TranslationFormSet = forms.formset_factory(TranslationForm, formset=TranslationFormSet, extra=0, can_delete=True)


class EditEntryView(PageView):
    page_template = 'dictionary/pages/edit_entry.html'
    fragment_template = 'dictionary/fragments/entry_deleted.html'
    get_entry_controller = GetEntry()
    edit_entry_controller = EditEntry()

    def get(self, request, entry_id, *args, **kwargs):
        entry = self.get_entry_controller.execute(entry_id)
        if not entry['id']:
            return self.render({}, **kwargs)

        context = {
            'entry': entry,
            'entry_form': EntryForm(entry),
            'translation_forms': TranslationFormSet(initial=entry['translations'])
        }
        return self.render(context, **kwargs)

    def post(self, request, entry_id, *args, **kwargs):
        entry = self.get_entry_controller.execute(entry_id)
        entry_form = EntryForm(request.POST)
        translation_forms = TranslationFormSet(request.POST, initial=entry['translations'])
        valid_entry = entry_form.is_valid()
        valid_translations = translation_forms.is_valid()
        if not valid_entry or not valid_translations:
            context = {
                'entry': entry,
                'entry_form': entry_form,
                'translation_forms': translation_forms
            }
            return self.render(context, **kwargs)

        self.edit_entry_controller.execute(
            entry_form.cleaned_data, translation_forms.get_translations_data()
        )

        return redirect('entry-view', entry_id=entry['id'])
