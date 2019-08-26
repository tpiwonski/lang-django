from lang.dictionary.models import Entry
from lang.dictionary.serializers import EditEntryOutput


class GetAllEntries(object):
    entry_repository = Entry.objects

    def execute(self):
        entries = self.entry_repository.get_all()
        return [EditEntryOutput(entry).data for entry in entries]
