import uuid

from django.db import models

from lang.dictionary.db.entry import EntryManager, EntryData, LANGUAGES, EntryRecordingData
# from lang.dictionary.models.translation import Translation


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
