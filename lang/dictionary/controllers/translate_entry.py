from lang.dictionary.integrations.diki.service import TranslationService
from lang.dictionary.models import Entry


class TranslateEntry(object):
    entry_repository = Entry.objects
    translation_service = TranslationService()

    def execute(self, text):
        results = self.translation_service.translate(text)
        return results

        # entries = []
        # for entry_data in results:
        #     entry = self.entry_repository.get_by_text(entry_data['text'], entry_data['language'])
        #     if not entry:
        #         entry = Entry.create(entry_data['text'], entry_data['language'])
        #         entry.add_recordings(entry_data['recordings'])
        #
        #     for translation_data in entry_data['translations']:
        #         translation = self.entry_repository.get_by_text(translation_data['text'], translation_data['language'])
        #         if not translation:
        #             translation = Entry.create(translation_data['text'], translation_data['language'])
        #
        #         if not entry.has_translation(translation):
        #             entry.add_translation(translation)
        #
        #     self.entry_repository.save(entry)
        #     entries.append(entry)
        #
        # return [EntryOutput(entry).data for entry in entries]
