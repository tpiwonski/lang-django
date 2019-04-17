import uuid

from lang.dictionary.db.translation import TranslationData


class Translation(TranslationData):

    class Meta:
        proxy = True

    @staticmethod
    def create(source, translated):
        return Translation(id=uuid.uuid4(), source=source, translated=translated)
