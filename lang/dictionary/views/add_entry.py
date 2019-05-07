from django import forms
from django.views.generic.base import View
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import redirect

from lang.dictionary.db.entry import LANGUAGES, LANGUAGE_EN, LANGUAGE_PL
from lang.common.component import ComponentContext, ComponentView
from lang.dictionary.controllers import AddEntry
from lang.dictionary.views.base import BaseContext


class EntryForm(forms.Form):
    text = forms.CharField(max_length=255)
    language = forms.ChoiceField(choices=LANGUAGES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['language'] = LANGUAGE_EN


class TranslationForm(forms.Form):
    text = forms.CharField(required=True)
    language = forms.ChoiceField(choices=LANGUAGES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['language'] = LANGUAGE_PL


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


TranslationFormSet = forms.formset_factory(TranslationForm, formset=TranslationFormSet, can_delete=True, extra=0)


class AddEntryView(ComponentView):
    template_name = 'dictionary/pages/add_entry.html'
    add_entry_controller = AddEntry()
    context_classes = [BaseContext]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'entry_form': EntryForm(),
            'translation_forms': TranslationFormSet()
        })
        return context

    def post(self, request, *args, **kwargs):
        entry_form = EntryForm(request.POST)
        translation_forms = TranslationFormSet(request.POST)
        valid_entry = entry_form.is_valid()
        valid_translations = translation_forms.is_valid()
        if not valid_entry or not valid_translations:
            context = super().get_context_data(**kwargs)
            context.update({
                'entry_form': entry_form,
                'translation_forms': translation_forms
            })
            return self.render_to_response(context)
        
        entry = self.add_entry_controller.execute(
            entry_form.cleaned_data, translation_forms.get_translations_data()
        )
        
        return redirect('entry-view', entry_id=entry['id'])
