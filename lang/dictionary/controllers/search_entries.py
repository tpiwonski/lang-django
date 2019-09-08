from lang.dictionary.models import Entry


class SearchEntries(object):
    entry_repository = Entry.objects

    def execute(self, text):
        entries = self.entry_repository.search_with_text(text)
        return entries
