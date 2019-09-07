import uuid

from lang.dictionary.db.synonym import SynonymModel


class Synonym(SynonymModel):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} - {}".format(self.subject, self.object)

    @staticmethod
    def create(object, subject):
        return Synonym.objects.create(id=uuid.uuid4(), object=object, subject=subject)
