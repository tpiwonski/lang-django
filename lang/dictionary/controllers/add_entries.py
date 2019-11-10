import itertools
from operator import attrgetter
from typing import List

from django.db import transaction

from lang.dictionary.db.entry import ENTRY_TYPE_SENTENCE
from lang.dictionary.models import Entry, Example, Recording
from lang.dictionary.data import EntryData


class AddEntries(object):
    entry_repository = Entry.objects
    example_repository = Example.objects
    recording_repository = Recording.objects

    @transaction.atomic
    def execute(self, entries_data: List[EntryData]):
        entries = []
        for entry_data in entries_data:
            headword_synonyms = []
            for headword_data in entry_data.headwords:
                for translation_data in entry_data.translations:
                    entry = self.entry_repository.get_by_text(headword_data.text, entry_data.language, translation_data.type)
                    if not entry:
                        entry = Entry.create(headword_data.text, entry_data.language, translation_data.type, headword_data.source_url)

                    headword_synonyms.append(entry)

                    for entry_recording_data in headword_data.recordings:
                        if not entry.has_recording(entry_recording_data.audio_url):
                            entry.add_recording(entry_recording_data.audio_url)

                    translation_synonyms = []
                    for translation_entry_data in translation_data.entries:
                        translation_entry = self.entry_repository.get_by_text(
                            translation_entry_data.text, translation_data.language, translation_data.type)
                        if not translation_entry:
                            translation_entry = Entry.create(
                                translation_entry_data.text, translation_data.language, translation_data.type,
                                translation_entry_data.source_url)

                        translation_synonyms.append(translation_entry)

                        translation = entry.get_translation(translation_entry)
                        if not translation:
                            translation = entry.add_translation(translation_entry)

                        for entry_recording_data in translation_data.recordings:
                            if not translation_entry.has_recording(entry_recording_data.audio_url):
                                translation_entry.add_recording(entry_recording_data.audio_url)

                        for example_data in translation_data.examples:
                            example = self.example_repository.get_by_text(example_data.text)
                            if not example:

                                example_entry = self.entry_repository.get_by_text(
                                    example_data.text, entry_data.language, ENTRY_TYPE_SENTENCE)
                                if not example_entry:
                                    example_entry = Entry.create(
                                        example_data.text, entry_data.language, ENTRY_TYPE_SENTENCE)

                                example_translation = self.entry_repository.get_by_text(
                                    example_data.translation, translation_data.language, ENTRY_TYPE_SENTENCE)
                                if not example_translation:
                                    example_translation = Entry.create(
                                        example_data.translation, translation_data.language, ENTRY_TYPE_SENTENCE)

                                if not example_translation.has_recording(example_data.recording.audio_url):
                                    example_translation.add_recording(example_data.recording.audio_url)

                                if not example_entry.get_translation(example_translation):
                                    example_entry.add_translation(example_translation)

                                example = Example.create(example_entry, example_translation)

                            if not translation.has_example(example):
                                translation.add_example(example)

                    for i, k in itertools.combinations(translation_synonyms, 2):
                        if not i.has_synonym(k):
                            i.add_synonym(k)

                    entries.append(entry)

            for k, g in itertools.groupby(sorted(headword_synonyms, key=attrgetter('type')), attrgetter('type')):
                for i, k in itertools.combinations(set(g), 2):
                    if not i.has_synonym(k):
                        i.add_synonym(k)

        return entries
