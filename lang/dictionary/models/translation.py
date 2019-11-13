import uuid

from lang.dictionary.db.translation import TranslationModel
from lang.dictionary.models.translation_example import TranslationExample


class Translation(TranslationModel):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} - {}".format(self.subject, self.object)

    @staticmethod
    def create(object, subject, usage_notes=''):
        return Translation.objects.create(
            id=uuid.uuid4(), object=object, subject=subject,
            usage_notes=usage_notes if usage_notes else '')

    def add_example(self, example):
        if self.has_example(example):
            raise Exception("Example already exists")

        return TranslationExample.create(translation=self, example=example)
