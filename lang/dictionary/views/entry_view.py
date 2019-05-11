from django.shortcuts import redirect, HttpResponse, render

from lang.common.component import ComponentView, ComponentContext
from lang.dictionary.controllers import GetEntry, DeleteEntry
from lang.dictionary.views.base import BaseContext


class EntryContext(ComponentContext):
    context_classes = [BaseContext]
    get_entry_controller = GetEntry()

    def get_context(self, request, entry_id, **kwargs):
        entry = self.get_entry_controller.execute(entry_id)
        return {
            'entry': entry
        }


class EntryView(ComponentView):
    page_template = 'dictionary/pages/entry_view.html'
    fragment_template = 'dictionary/fragments/entry_deleted.html'
    context_classes = [EntryContext]
    delete_entry_controller = DeleteEntry()

    def get(self, request, *args, **kwargs):
        return self.render_page({}, **kwargs)

    def delete(self, request, entry_id, *args, **kwargs):
        self.delete_entry_controller.execute(entry_id)
        return self.render_fragment({}, **kwargs)
