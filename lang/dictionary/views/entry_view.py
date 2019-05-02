from lang.common.component import ComponentView, ComponentContext
from lang.dictionary.controllers import GetEntry
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
    template_name = 'dictionary/pages/entry_view.html'
    context_classes = [EntryContext]
