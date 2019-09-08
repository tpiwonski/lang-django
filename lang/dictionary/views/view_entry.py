from lang.common.component import ComponentView
from lang.dictionary.controllers.view_entry import ViewEntry as ViewEntryController
from lang.dictionary.serializers import ViewEntryOutput


class ViewEntry(ComponentView):
    page_template = 'dictionary/pages/view_entry.html'
    view_entry_controller = ViewEntryController()

    def get(self, request, entry_id, *args, **kwargs):
        entry = self.view_entry_controller.execute(entry_id)
        context = {
            'entry': ViewEntryOutput(entry).data
        }
        return self.render(context, **kwargs)
