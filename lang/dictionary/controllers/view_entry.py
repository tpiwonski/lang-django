from lang.dictionary.models import Entry


class ViewEntry(object):
    entry_repository = Entry.objects

    def execute(self, entry_id):
        entry = self.entry_repository.get_by_id(entry_id)
        return entry
