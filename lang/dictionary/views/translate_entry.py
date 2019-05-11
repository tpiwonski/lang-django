from django import forms
from django.shortcuts import redirect, render


from lang.dictionary.db.entry import LANGUAGES, LANGUAGE_EN, LANGUAGE_PL
from lang.common.component import ComponentContext, ComponentView
from lang.dictionary.views.base import BaseContext
from lang.dictionary.controllers import TranslateEntry


class TranslateForm(forms.Form):
    text = forms.CharField(max_length=255)


class TranslateEntryView(ComponentView):
    page_template = 'dictionary/pages/translate_entry.html'
    fragment_template = 'dictionary/fragments/translate_entry.html'
    context_classes = [BaseContext]
    translate_entry_controller = TranslateEntry()

    def get(self, request, *args, **kwargs):
        context = {
            'translate_form': TranslateForm()
        }
        return self.render_page(context, **kwargs)

    def post(self, request, *args, **kwargs):
        translate_form = TranslateForm(request.POST)
        if not translate_form.is_valid():
            context = {
                'translate_form': translate_form
            }
            return self.render_fragment(context, **kwargs)
        
        entries = self.translate_entry_controller.execute(**translate_form.cleaned_data)

        context = {
            'translate_form': translate_form,
            'entries': entries
        }
        return self.render_fragment(context, **kwargs)
