from lang.common.component import ComponentView
from lang.dictionary.controllers.view_all_entries import ViewAllEntries as ViewAllEntriesController


class ViewAllEntries(ComponentView):
    page_template = 'dictionary/pages/view_all_entries.html'
    get_all_entries_controller = ViewAllEntriesController()

    def get(self, request, *args, **kwargs):
        entries = self.get_all_entries_controller.execute()
        context = {
            'entries': entries
        }
        return self.render(context, **kwargs)
