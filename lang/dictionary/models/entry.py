import uuid

from django.db import models

from lang.dictionary.db.entry import EntryManager, EntryData, LANGUAGES
from lang.dictionary.models.translation import Translation


class Entry(EntryData):

    class Meta:
        proxy = True

    @staticmethod
    def create(text, language):
        return Entry(id=uuid.uuid4(), text=text, language=language)

    def add_translation(self, translated_entry):
        if self.has_translation(translated_entry):
            return

        translation = Translation.create(source=self, translated=translated_entry)
        self._add_translation(translation)

    def has_translation(self, translated_entry):
        return any([t for t in self.translations 
                    if t.text == translated_entry.text and t.language == translated_entry.language])
