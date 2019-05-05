from django import forms
from django.shortcuts import redirect, render

from lang.common.component import ComponentView
from lang.dictionary.controllers import SearchEntries
from lang.dictionary.db.entry import LANGUAGES, LANGUAGE_EN
from lang.dictionary.views.base import BaseContext


class SearchEntriesForm(forms.Form):
    text = forms.CharField(max_length=255)
    # language = forms.ChoiceField(choices=LANGUAGES)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.initial['language'] = LANGUAGE_EN


class SearchEntriesView(ComponentView):
    template_name = 'dictionary/pages/search_entries.html'
    context_classes = [BaseContext]
    search_entries_controller = SearchEntries()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_form': SearchEntriesForm()
        })
        return context

    def post(self, request, *args, **kwargs):
        search_form = SearchEntriesForm(request.POST)
        if not search_form.is_valid():
            context = super().get_context_data(**kwargs)
            context.update({
                'search_form': search_form
            })
            return render(request, 'dictionary/fragments/search_entries.html', context)
            # return self.render_to_response(context)

        entries = self.search_entries_controller.execute(**search_form.cleaned_data)
        
        context = super().get_context_data(**kwargs)
        context.update({
            'search_form': search_form,
            'entries': entries
        })
        return render(request, 'dictionary/fragments/search_entries.html', context)
