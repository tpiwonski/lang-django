import uuid

from lang.dictionary.db.example import ExampleData, RelationExampleData


class RelationExample(RelationExampleData):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} - {}".format(self.relation, self.example)

    @staticmethod
    def create(relation, example):
        return RelationExample(id=uuid.uuid4(), relation=relation, example=example)


class Example(ExampleData):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} - {}".format(self.subject, self.object)

    @staticmethod
    def create(entry, translation):
        return Example(id=uuid.uuid4(), object=entry, subject=translation)
