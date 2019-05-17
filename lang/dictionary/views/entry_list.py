from lang.dictionary.controllers import GetAllEntries
from lang.dictionary.views.base import PageView


class EntryListView(PageView):
    page_template = 'dictionary/pages/entry_list.html'
    get_all_entries_controller = GetAllEntries()

    def get(self, request, *args, **kwargs):
        entries = self.get_all_entries_controller.execute()
        context = {
            'entries': entries
        }
        return self.render(context, **kwargs)
