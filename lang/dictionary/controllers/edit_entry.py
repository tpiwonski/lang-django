from lang.dictionary.models import Entry


class EditEntry(object):
    entry_repository = Entry.objects

    def execute(self, entry_data, translations_data):
        entry = self.entry_repository.get_by_id(entry_data['id'])
        entry.text = entry_data['text']
        entry.language = entry_data['language']
        entry.type = entry_data['type']

        for translation in entry.translated_entries:
            if translation.id not in [t['id'] for t in translations_data]:
                entry.remove_translation(translation)

        for translation_data in translations_data:
            if not translation_data['id']:
                translation = self.entry_repository.get_by_text(translation_data['text'], translation_data['language'], translation_data['type'])
                if not translation:
                    translation = Entry.create(translation_data['text'], translation_data['language'], translation_data['type'])

                if not entry.has_translation(translation):
                    entry.add_translation(translation)

            else:
                translation = self.entry_repository.get_by_id(translation_data['id'])
                translation.text = translation_data['text']
                translation.language = translation_data['language']
                translation.type = translation_data['type']
                translation.save()

                if not entry.has_translation(translation):
                    entry.add_translation(translation)

        entry.save()
        return entry
