import uuid

from django.db.models import Q

from lang.dictionary.db.entry import EntryModel
from lang.dictionary.models.synonym import Synonym
from lang.dictionary.models.recording import Recording
from lang.dictionary.models.translation import Translation


class Entry(EntryModel):

    class Meta:
        proxy = True

    def __str__(self):
        return "{}".format(self.text)

    @staticmethod
    def create(text, language, entry_type, source_url=''):
        return Entry.objects.create(id=uuid.uuid4(), text=text, language=language, type=entry_type, source_url=source_url)

    def add_translation(self, entry, collocations=None):
        if self.has_translation(entry):
            raise Exception("Translation already exists")

        return Translation.create(
            object=self, subject=entry, collocations=collocations)

    def remove_translation(self, entry):
        Translation.objects.filter(Q(object=self, subject=entry) | Q(object=entry, subject=self)).delete()

    def add_recording(self, url):
        return Recording.create(self, url)

    def add_synonym(self, entry):
        if self.has_synonym(entry):
            raise Exception("Synonym already exists")

        return Synonym.create(object=self, subject=entry)
