from lang.dictionary.models import Entry


class DeleteEntry(object):
    entry_repository = Entry.objects

    def execute(self, entry_id):
        self.entry_repository.delete(entry_id)
