from django import forms
from django.shortcuts import redirect


from lang.dictionary.db.entry import LANGUAGES, LANGUAGE_EN, LANGUAGE_PL
from lang.common.component import ComponentContext, ComponentView
from lang.dictionary.views.base import BaseContext
from lang.dictionary.controllers import TranslateEntry


class EntryForm(forms.Form):
    text = forms.CharField(max_length=255)
    language = forms.ChoiceField(choices=LANGUAGES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['language'] = LANGUAGE_EN


class TranslateEntryView(ComponentView):
    template_name = 'dictionary/pages/translate_entry.html'
    context_classes = [BaseContext]
    translate_entry_controller = TranslateEntry()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'entry_form': EntryForm()
        })
        return context

    def post(self, request, *args, **kwargs):
        entry_form = EntryForm(request.POST)
        if not entry_form.is_valid():
            context = super().get_context_data(**kwargs)
            context.update({
                'entry_form': entry_form
            })
            return self.render_to_response(context)
        
        self.translate_entry_controller.execute(entry_form.cleaned_data)

        return redirect('entry-list')

        # return redirect('entry-view', entry_id=entry['id'])