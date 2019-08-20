import uuid

from lang.dictionary.models import Entry, Example
from lang.dictionary.serializers import EntryOutput, AddEntryOutput
from lang.dictionary.integrations.diki.service import TranslationService

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


class SearchEntries(object):
    entry_repository = Entry.objects

    def execute(self, text):
        entries = self.entry_repository.search_with_text(text)
        return [EntryOutput(entry).data for entry in entries]


class AddEntry(object):
    entry_repository = Entry.objects

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
        return EntryOutput(entry).data


class EditEntry(object):
    entry_repository = Entry.objects

    def execute(self, entry_data, translations_data):
        entry = self.entry_repository.get_by_id(entry_data['id'])
        entry.text = entry_data['text']
        entry.language = entry_data['language']

        for translation in entry.translations:
            if translation.id not in [t['id'] for t in translations_data]:
                entry.remove_translation(translation)

        for translation_data in translations_data:
            if not translation_data['id']:
                translation = self.entry_repository.get_by_text(translation_data['text'], translation_data['language'])
                if not translation:
                    translation = Entry.create(translation_data['text'], translation_data['language'])

                if not entry.has_translation(translation):
                    entry.add_translation(translation)
            
            else:
                translation = self.entry_repository.get_by_id(translation_data['id'])
                translation.text = translation_data['text']
                translation.language = translation_data['language']

                if not entry.has_translation(translation):
                    entry.add_translation(translation)

        self.entry_repository.save(entry)
        return EntryOutput(entry).data


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


class AddEntries(object):
    entry_repository = Entry.objects
    example_repository = Example.objects

    def execute(self, results):
        entries = []
        for entry_data in results:
            entry = self.entry_repository.get_by_text(entry_data['text'], entry_data['language'])
            if not entry:
                entry = Entry.create(entry_data['text'], entry_data['language'])
                # entry.add_recordings(entry_data['recordings'])

            for translation_data in entry_data['translations']:
                translation = self.entry_repository.get_by_text(translation_data['text'], translation_data['language'])
                if not translation:
                    translation = Entry.create(translation_data['text'], translation_data['language'])

                # if not entry.has_translation(translation):
                relation = entry.get_translation(translation)
                if not relation:
                    relation = entry.add_translation(translation)

                for example_data in translation_data.get('examples', []):
                    example = self.example_repository.get_by_text(example_data['text'])
                    if not example:

                        example_entry = self.entry_repository.get_by_text(example_data['text'], entry_data['language'])
                        if not example_entry:
                            example_entry = Entry.create(example_data['text'], entry_data['language'])

                        example_translation = self.entry_repository.get_by_text(example_data['translation'], translation_data['language'])
                        if not example_translation:
                            example_translation = Entry.create(example_data['translation'], translation_data['language'])

                        example_relation = example_entry.get_translation(example_translation)
                        if not example_relation:
                            example_relation = example_entry.add_translation(example_translation)

                        example = Example.create(example_entry, example_translation)

                    relation_example = relation.get_example(example)
                    if not relation_example:
                        relation_example = relation.add_example(example)

                    # example_entry = self.entry_repository.get_by_text(example['text'], entry_data['language'])
                    # if not example_entry:
                    #     example_entry = Entry.create(example['text'], entry_data['language'])
                    #
                    # example_translation = self.entry_repository.get_by_text(example['translation'], translation_data['language'])
                    # if not example_translation:
                    #     example_translation = Entry.create(example['translation'], translation_data['language'])
                    #
                    # if not example_entry.has_translation(example_translation):
                    #     example_entry.add_translation(example_translation)

                    # self.entry_repository.save(example_entry)
                    #
                    # if not translation.has_example(example_entry):
                    #     translation.add_example(example_entry)

                    # entry.add_example(translation, example['text'], example['translation'])

                # self.entry_repository.save(translation)
                self.entry_repository.save(entry)

            # self.entry_repository.save(entry)
            entries.append(entry)

        return [EntryOutput(entry).data for entry in entries]


class DeleteEntry(object):
    entry_repository = Entry.objects

    def execute(self, entry_id):
        self.entry_repository.delete(entry_id)
