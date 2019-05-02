import uuid

from lang.dictionary.models import Entry
from lang.dictionary.serializers import EntryOutput, AddEntryOutput
from lang.dictionary.services.diki.service import TranslationService

# class AddEntry(object):
#     entry_repository = Entry.objects

#     def execute(self, text, language):
#         entry = Entry.create(text=text, language=language)
#         self.entry_repository.save(entry)
#         return EntryOutput(entry).data


class GetEntry(object):
    entry_repository = Entry.objects

    def execute(self, entry_id):
        entry = self.entry_repository.get_by_id(entry_id)
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


class AddEntry(object):
    entry_repository = Entry.objects

    def execute(self, entry_data, translations_data):
        entry = self.entry_repository.find(entry_data['text'], entry_data['language'])
        if entry:
            entry = entry[0]
        else:
            entry = Entry.create(entry_data['text'], entry_data['language'])

        for translation_data in translations_data:
            translation = self.entry_repository.find(translation_data['text'], translation_data['language'])
            if translation:
                translation = translation[0]
            else:
                translation = Entry.create(translation_data['text'], translation_data['language'])

            if not entry.has_translation(translation):
                entry.add_translation(translation)

        self.entry_repository.save(entry)
        return EntryOutput(entry).data


class EditEntry(object):
    entry_repository = Entry.objects

    def execute(self, entry_data, translations_data):
        entry = self.entry_repository.get_by_id(entry_data['id'])
        entry.text = entry_data['text']

        for translation in entry.translations:
            if translation.id not in [t['id'] for t in translations_data]:
                entry.remove_translation(translation)

        for translation_data in translations_data:
            if not translation_data['id']:
                translation = self.entry_repository.find(translation_data['text'], translation_data['language'])
                if translation:
                    translation = translation[0]
                else:
                    translation = Entry.create(translation_data['text'], translation_data['language'])

                if not entry.has_translation(translation):
                    entry.add_translation(translation)
            
            else:
                translation = self.entry_repository.get_by_id(translation_data['id'])
                translation.text = translation_data['text']

                if not entry.has_translation(translation):
                    entry.add_translation(translation)

        self.entry_repository.save(entry)
        return EntryOutput(entry).data


class TranslateEntry(object):
    entry_repository = Entry.objects
    translation_service = TranslationService()

    def execute(self, entry_data):
        results = self.translation_service.translate(entry_data['text'])
        for entry_data in results:
            entry = self.entry_repository.find(entry_data['text'], entry_data['language'])
            if entry:
                entry = entry[0]
            else:
                entry = Entry.create(entry_data['text'], entry_data['language'])

            for translation_data in entry_data['translations']:
                translation = self.entry_repository.find(translation_data['text'], translation_data['language'])
                if translation:
                    translation = translation[0]
                else:
                    translation = Entry.create(translation_data['text'], translation_data['language'])

                if not entry.has_translation(translation):
                    entry.add_translation(translation)
        
            self.entry_repository.save(entry)
