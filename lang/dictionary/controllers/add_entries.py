import itertools

from django.db import transaction

from lang.dictionary.db.entry import ENTRY_TYPE_SENTENCE
from lang.dictionary.models import Entry, Example, Recording


class AddEntries(object):
    entry_repository = Entry.objects
    example_repository = Example.objects
    recording_repository = Recording.objects

    @transaction.atomic
    def execute(self, results):
        entries = []
        for entry_data in results:
            entry = self.entry_repository.get_by_text(entry_data['text'], entry_data['language'], entry_data['type'])
            if not entry:
                entry = Entry.create(entry_data['text'], entry_data['language'], entry_data['type'])

            for entry_recording_data in entry_data['recordings']:
                if not entry.has_recording(entry_recording_data['url']):
                    entry.add_recording(entry_recording_data['url'])

            for translation_data in entry_data['translations']:
                synonyms = []
                for translation_entry in translation_data['entries']:
                    translation = self.entry_repository.get_by_text(translation_entry['text'], translation_data['language'], translation_data['type'])
                    if not translation:
                        translation = Entry.create(translation_entry['text'], translation_data['language'], translation_data['type'])

                    synonyms.append(translation)

                    relation = entry.get_translation(translation)
                    if not relation:
                        relation = entry.add_translation(translation)

                    for entry_recording_data in translation_data['recordings']:
                        if not translation.has_recording(entry_recording_data['url']):
                            translation.add_recording(entry_recording_data['url'])

                    for example_data in translation_data.get('examples', []):
                        example = self.example_repository.get_by_text(example_data['text'])
                        if not example:

                            example_entry = self.entry_repository.get_by_text(example_data['text'], entry_data['language'], ENTRY_TYPE_SENTENCE)
                            if not example_entry:
                                example_entry = Entry.create(example_data['text'], entry_data['language'], ENTRY_TYPE_SENTENCE)

                            example_translation = self.entry_repository.get_by_text(example_data['translation'], translation_data['language'], ENTRY_TYPE_SENTENCE)
                            if not example_translation:
                                example_translation = Entry.create(example_data['translation'], translation_data['language'], ENTRY_TYPE_SENTENCE)

                            if not example_translation.has_recording(example_data['recording']['url']):
                                example_translation.add_recording(example_data['recording']['url'])

                            if not example_entry.get_translation(example_translation):
                                example_entry.add_translation(example_translation)

                            example = Example.create(example_entry, example_translation)

                        if not relation.has_example(example):
                            relation.add_example(example)

                for i, k in itertools.combinations(synonyms, 2):
                    if not i.has_synonym(k):
                        i.add_synonym(k)

            entries.append(entry)

        return entries
