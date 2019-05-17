from lang.dictionary.controllers import GetEntry
from lang.dictionary.views.base import PageView


class EntryView(PageView):
    page_template = 'dictionary/pages/view_entry.html'
    get_entry_controller = GetEntry()

    def get(self, request, entry_id, *args, **kwargs):
        entry = self.get_entry_controller.execute(entry_id)
        context = {
            'entry': entry
        }
        return self.render_page(context, **kwargs)
