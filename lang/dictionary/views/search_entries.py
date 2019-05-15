import json

from django import forms
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.http import HttpResponse

from lang.common.component import ComponentView
from lang.dictionary.controllers import SearchEntries
from lang.dictionary.db.entry import LANGUAGES, LANGUAGE_EN
from lang.dictionary.views.base import BaseContext
from lang.dictionary.views.current_date import CurrentDateView


class SearchEntriesForm(forms.Form):
    q = forms.CharField(max_length=255)


class SearchEntriesView(ComponentView):
    fragment_id = 'search-entries'
    page_template = 'dictionary/pages/search_entries.html'
    fragment_template = 'dictionary/fragments/search_entries.html'
    context_classes = [BaseContext]
    component_classes = [CurrentDateView]
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

        return self.render(context, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     search_form = SearchEntriesForm(request.POST)
    #     context = {
    #         'search_form': search_form
    #     }
    #     if not search_form.is_valid():
    #         return self.render_fragment(context, **kwargs)

    #     entries = self.search_entries_controller.execute(text=search_form.cleaned_data['q'])
    #     context.update({
    #         'entries': entries
    #     })
    #     # return self.render_fragment(context, **kwargs)

    #     return self.render_response(context, [CurrentDateView, SearchEntriesView], **kwargs)

        # return self.render_response(context, {
        #     'current-date': 'dictionary/fragments/current_date.html',
        #     'search-entries': self.fragment_template
        # }, **kwargs)

        # context.update(self.get_context_data(**kwargs))
        # content = {
        #     'current-date': render_to_string('dictionary/fragments/current_date.html', context, request),
        #     'search-entries': render_to_string(self.fragment_template, context, request)
        # }
        
        # return HttpResponse(json.dumps(content), content_type="application/json")
