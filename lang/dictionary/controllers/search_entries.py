from lang.dictionary.models import Entry
from lang.dictionary.serializers import ViewEntryOutput


class SearchEntries(object):
    entry_repository = Entry.objects

    def execute(self, text):
        entries = self.entry_repository.search_with_text(text)
        return [ViewEntryOutput(entry).data for entry in entries]
