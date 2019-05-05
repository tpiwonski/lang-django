from django import forms
from django.shortcuts import redirect, render


from lang.dictionary.db.entry import LANGUAGES, LANGUAGE_EN, LANGUAGE_PL
from lang.common.component import ComponentContext, ComponentView
from lang.dictionary.views.base import BaseContext
from lang.dictionary.controllers import TranslateEntry


class TranslateForm(forms.Form):
    text = forms.CharField(max_length=255)
    # language = forms.ChoiceField(choices=LANGUAGES)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.initial['language'] = LANGUAGE_EN


class TranslateEntryView(ComponentView):
    template_name = 'dictionary/pages/translate_entry.html'
    context_classes = [BaseContext]
    translate_entry_controller = TranslateEntry()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'translate_form': TranslateForm()
        })
        return context

    def post(self, request, *args, **kwargs):
        translate_form = TranslateForm(request.POST)
        if not translate_form.is_valid():
            context = super().get_context_data(**kwargs)
            context.update({
                'translate_form': translate_form
            })
            return render(request, 'dictionary/fragments/translate_entry.html', context)
            # return self.render_to_response(context)
        
        entries = self.translate_entry_controller.execute(**translate_form.cleaned_data)

        context = super().get_context_data(**kwargs)
        context.update({
            'translate_form': translate_form,
            'entries': entries
        })
        return render(request, 'dictionary/fragments/translate_entry.html', context)
