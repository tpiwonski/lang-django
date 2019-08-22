import uuid

from lang.dictionary.db.translation import TranslationModel


class Translation(TranslationModel):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} - {}".format(self.subject, self.object)

    @staticmethod
    def create(object, subject):
        return Translation(id=uuid.uuid4(), object=object, subject=subject)
