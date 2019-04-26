from lang.component import ComponentContext, ComponentView
from lang.dictionary.controllers import GetAllEntries
from lang.dictionary.views.current_date import CurrentDateContext


class EntryListContext(ComponentContext):
    get_all_entries_controller = GetAllEntries()

    def get_context(self, request, **kwargs):
        context = super(EntryListContext, self).get_context(request, **kwargs)
        entries = self.get_all_entries_controller.execute()
        context['entries'] = entries
        return context


class EntryListView(
    EntryListContext, 
    CurrentDateContext, 
    ComponentView
):
    template_name = 'dictionary/pages/entry_list.html'
