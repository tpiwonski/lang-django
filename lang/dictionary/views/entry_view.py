from lang.common.component import ComponentView
from lang.dictionary.controllers import GetEntry
from lang.dictionary.views.current_date import CurrentDateContext


class EntryContext(object):
    get_entry_controller = GetEntry()

    def get_context(self, request, entry_id, **kwargs):
        entry = self.get_entry_controller.execute(entry_id)
        return {
            'entry': entry
        }


class EntryView(ComponentView):
    template_name = 'dictionary/pages/entry_view.html'
    context_classes = [EntryContext, CurrentDateContext]
