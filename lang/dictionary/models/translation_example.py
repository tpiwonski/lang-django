import uuid

from lang.dictionary.db.translation_example import TranslationExampleModel


class TranslationExample(TranslationExampleModel):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} - {}".format(self.translation, self.example)

    @staticmethod
    def create(translation, example):
        return TranslationExample.objects.create(id=uuid.uuid4(), translation=translation, example=example)
