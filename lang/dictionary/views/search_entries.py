from django import forms
from django.shortcuts import redirect, render

from lang.common.component import ComponentView
from lang.dictionary.controllers import SearchEntries
from lang.dictionary.db.entry import LANGUAGES, LANGUAGE_EN
from lang.dictionary.views.base import BaseContext


class SearchEntriesForm(forms.Form):
    q = forms.CharField(max_length=255)


class SearchEntriesView(ComponentView):
    page_template = 'dictionary/pages/search_entries.html'
    fragment_template = 'dictionary/fragments/search_entries.html'
    context_classes = [BaseContext]
    search_entries_controller = SearchEntries()

    def get(self, request, *args, **kwargs):
        text = self.request.GET.get('q')
        search_form = SearchEntriesForm(initial={
            'q': text
        })
        context = {
            'search_form': search_form
        }

        if text:
            entries = self.search_entries_controller.execute(text)
            context.update({
                'entries': entries
            })

        return self.render_page(context, **kwargs)

    def post(self, request, *args, **kwargs):
        search_form = SearchEntriesForm(request.POST)
        context = {
            'search_form': search_form
        }
        if not search_form.is_valid():
            return self.render_fragment(context, **kwargs)

        entries = self.search_entries_controller.execute(text=search_form.cleaned_data['q'])
        context.update({
            'entries': entries
        })
        return self.render_fragment(context, **kwargs)
