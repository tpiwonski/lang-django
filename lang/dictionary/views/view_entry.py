from django.shortcuts import redirect, HttpResponse, render
from django.contrib import messages

from lang.common.component import ComponentView, ComponentContext
from lang.dictionary.controllers import GetEntry
from lang.dictionary.views.base import BaseContext


class EntryContext(ComponentContext):
    context_classes = [BaseContext]
    get_entry_controller = GetEntry()

    def get_context(self, request, entry_id, **kwargs):
        entry = self.get_entry_controller.execute(entry_id)
        if not entry['id']:
            return {}

        return {
            'entry': entry
        }


class EntryView(ComponentView):
    page_template = 'dictionary/pages/view_entry.html'
    entry_does_not_exist = 'dictionary/pages/entry_does_not_exist.html'
    context_classes = [EntryContext]

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'entry' not in context:
            return self.render(self.entry_does_not_exist, {}, **kwargs)

        return self.render_page(context, **kwargs)
