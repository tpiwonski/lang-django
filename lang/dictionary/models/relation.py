import uuid

from lang.dictionary.db.relation import RelationData, RELATION_KIND_SYNONYM, RELATION_KIND_TRANSLATION


class Relation(RelationData):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} - {} {}".format(self.subject, self.object, self.kind)

    @staticmethod
    def create(object, subject,  kind):
        return Relation(id=uuid.uuid4(), object=object, subject=subject, kind=kind)
