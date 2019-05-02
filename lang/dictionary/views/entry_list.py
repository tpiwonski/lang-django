from lang.common.component import ComponentView, ComponentContext
from lang.dictionary.controllers import GetAllEntries
from lang.dictionary.views.base import BaseContext


class EntryListContext(ComponentContext):
    context_classes = [BaseContext]
    get_all_entries_controller = GetAllEntries()

    def get_context(self, request, **kwargs):
        entries = self.get_all_entries_controller.execute()
        return {
            'entries': entries
        }


class EntryListView(ComponentView):
    template_name = 'dictionary/pages/entry_list.html'
    context_classes = [EntryListContext]
