import uuid
from dataclasses import dataclass
from typing import List

from lang.dictionary.db.entry import EntryData, EntryRecordingData, LANGUAGES
# from lang.models import Example


class Entry(EntryData):

    class Meta:
        proxy = True

    @staticmethod
    def create(text, language):
        return Entry(id=uuid.uuid4(), text=text, language=language)

    def add_translation(self, entry):
        if self.has_translation(entry):
            return None

        return super().add_translation(entry)

    def has_translation(self, entry):
        return any([t for t in self.translations 
                    if t.text == entry.text and t.language == entry.language])

    def add_recordings(self, recordings_data):
        for recording_data in recordings_data:
            self.add_recording(EntryRecordingData(id=uuid.uuid4(), entry=self, url=recording_data['url']))

    @property
    def foo_translations(self):
        from lang.dictionary.db.relation import RELATION_KIND_TRANSLATION
        return ([EntryTranslation(t.subject, [e.example for e in t.relation_examples.all()]) for t in self.related_subjects.filter(kind=RELATION_KIND_TRANSLATION)] +
                [EntryTranslation(t.object, [e.example for e in t.relation_examples.all()]) for t in self.related_objects.filter(kind=RELATION_KIND_TRANSLATION)] +
                [EntryTranslation(t.subject, [e.example for e in t.relation_examples.all()]) for t in self._add_translations])


@dataclass
class EntryTranslation:
    entry: Entry
    examples: List[int]
