import uuid

from lang.dictionary.models import Entry
from lang.dictionary.serializers import EntryOutput, AddTranslationOutput


class AddEntry(object):
    entry_repository = Entry.objects

    def execute(self, text, language):
        entry = Entry.create(text=text, language=language)
        self.entry_repository.save(entry)
        return EntryOutput(entry).data


class GetEntry(object):
    entry_repository = Entry.objects

    def execute(self, guid):
        entry = self.entry_repository.get_by_id(guid)
        return EntryOutput(entry).data


class GetAllEntries(object):
    entry_repository = Entry.objects

    def execute(self):
        entries = self.entry_repository.get_all()
        return [EntryOutput(entry).data for entry in entries]


class FindEntry(object):
    entry_repository = Entry.objects

    def execute(self, text, language=None):
        entries = self.entry_repository.find(text, language)
        return [EntryOutput(entry).data for entry in entries]


class AddTranslation(object):
    entry_repository = Entry.objects

    def execute(self, entry, translations):
        source_entry = self.entry_repository.find(entry['text'], entry['language'])
        if source_entry:
            source_entry = source_entry[0]
        else:
            source_entry = Entry.create(entry['text'], entry['language'])

        for translation in translations:
            translated_entry = self.entry_repository.find(translation['text'], translation['language'])
            if translated_entry:
                translated_entry = translated_entry[0]
            else:
                translated_entry = Entry.create(translation['text'], translation['language'])

            if not source_entry.has_translation(translated_entry):
                source_entry.add_translation(translated_entry)

        self.entry_repository.save(source_entry)
        return AddTranslationOutput(source_entry).data
