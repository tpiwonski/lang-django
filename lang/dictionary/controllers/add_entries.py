from django.db import transaction

from lang.dictionary.db.entry import ENTRY_TYPE_SENTENCE
from lang.dictionary.models import Entry, Example
from lang.dictionary.serializers import ViewEntryOutput


class AddEntries(object):
    entry_repository = Entry.objects
    example_repository = Example.objects

    @transaction.atomic
    def execute(self, results):
        entries = []
        for entry_data in results:
            entry = self.entry_repository.get_by_text(entry_data['text'], entry_data['language'], entry_data['type'])
            if not entry:
                entry = Entry.create(entry_data['text'], entry_data['language'], entry_data['type'])
                # entry.add_recordings(entry_data['recordings'])

            for translation_data in entry_data['translations']:
                translation = self.entry_repository.get_by_text(translation_data['text'], translation_data['language'], translation_data['type'])
                if not translation:
                    translation = Entry.create(translation_data['text'], translation_data['language'], translation_data['type'])

                # if not entry.has_translation(translation):
                relation = entry.get_translation(translation)
                if not relation:
                    relation = entry.add_translation(translation)

                for example_data in translation_data.get('examples', []):
                    example = self.example_repository.get_by_text(example_data['text'])
                    if not example:

                        example_entry = self.entry_repository.get_by_text(example_data['text'], entry_data['language'], ENTRY_TYPE_SENTENCE)
                        if not example_entry:
                            example_entry = Entry.create(example_data['text'], entry_data['language'], ENTRY_TYPE_SENTENCE)

                        example_translation = self.entry_repository.get_by_text(example_data['translation'], translation_data['language'], ENTRY_TYPE_SENTENCE)
                        if not example_translation:
                            example_translation = Entry.create(example_data['translation'], translation_data['language'], ENTRY_TYPE_SENTENCE)

                        example_relation = example_entry.get_translation(example_translation)
                        if not example_relation:
                            example_relation = example_entry.add_translation(example_translation)

                        example = Example.create(example_entry, example_translation)

                    # relation_example = relation.get_example(example)
                    if not relation.has_example(example):
                        relation.add_example(example)

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

        return [ViewEntryOutput(entry).data for entry in entries]
