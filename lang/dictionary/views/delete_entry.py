from lang.common.component import ComponentView
from lang.dictionary.controllers.delete_entry import DeleteEntry


class DeleteEntryView(ComponentView):
    fragment_template = 'dictionary/fragments/entry_deleted.html'
    delete_entry_controller = DeleteEntry()

    def post(self, request, entry_id, *args, **kwargs):
        self.delete_entry_controller.execute(entry_id)
        return self.render({}, **kwargs)
