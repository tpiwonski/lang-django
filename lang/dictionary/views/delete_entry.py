from django.shortcuts import redirect, HttpResponse, render
from django.contrib import messages

from lang.common.component import ComponentView, ComponentContext
from lang.dictionary.controllers import DeleteEntry
from lang.dictionary.views.base import BaseContext


class DeleteEntryView(ComponentView):
    fragment_template = 'dictionary/fragments/entry_deleted.html'
    context_classes = [BaseContext]
    delete_entry_controller = DeleteEntry()

    def post(self, request, entry_id, *args, **kwargs):
        self.delete_entry_controller.execute(entry_id)
        return self.render_fragment({}, **kwargs)
