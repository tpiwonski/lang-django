from lang.component import ComponentContext, ComponentView
from lang.dictionary.controllers import GetEntry


class EntryContext(ComponentContext):
    get_entry_controller = GetEntry()

    def get_context(self, request, entry_id, **kwargs):
        context = super().get_context(request, **kwargs)
        entry = self.get_entry_controller.execute(entry_id)
        context['entry'] = entry
        return context


class EntryView(EntryContext, ComponentView):
    template_name = 'dictionary/pages/entry_view.html'
