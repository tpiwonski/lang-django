import uuid

from lang.dictionary.db.example import ExampleData


class Example(ExampleData):

    class Meta:
        proxy = True

    @staticmethod
    def create(entry, example):
        return Example(id=uuid.uuid4(), entry=entry, example=example)
