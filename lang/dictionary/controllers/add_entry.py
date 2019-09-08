from django.db import transaction

from lang.dictionary.models import Entry


class AddEntry(object):
    entry_repository = Entry.objects

    @transaction.atomic
    def execute(self, entry_data, translations_data):
        entry = self.entry_repository.get_by_text(entry_data['text'], entry_data['language'])
        if not entry:
            entry = Entry.create(entry_data['text'], entry_data['language'])

        for translation_data in translations_data:
            translation = self.entry_repository.get_by_text(translation_data['text'], translation_data['language'])
            if not translation:
                translation = Entry.create(translation_data['text'], translation_data['language'])

            if not entry.has_translation(translation):
                entry.add_translation(translation)

        self.entry_repository.save(entry)
        return entry
