from lang.dictionary.models import Entry


class GetAllEntries(object):
    entry_repository = Entry.objects

    def execute(self):
        entries = self.entry_repository.get_all()
        return entries
