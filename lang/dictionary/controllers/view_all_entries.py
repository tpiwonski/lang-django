from lang.dictionary.models import Entry
from lang.dictionary.serializers import ViewEntryOutput


class ViewAllEntries(object):
    entry_repository = Entry.objects

    def execute(self):
        entries = self.entry_repository.get_all()
        return [ViewEntryOutput(entry).data for entry in entries]
