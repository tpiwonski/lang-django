from lang.dictionary.controllers.delete_entry import DeleteEntry
from lang.dictionary.views.base import PageView


class DeleteEntryView(PageView):
    fragment_template = 'dictionary/fragments/entry_deleted.html'
    # context_classes = [BaseContext]
    delete_entry_controller = DeleteEntry()

    def post(self, request, entry_id, *args, **kwargs):
        self.delete_entry_controller.execute(entry_id)
        return self.render({}, **kwargs)
