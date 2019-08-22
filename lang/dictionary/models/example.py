import uuid

from lang.dictionary.db.example import ExampleModel


class Example(ExampleModel):

    class Meta:
        proxy = True

    def __str__(self):
        return "{} - {}".format(self.subject, self.object)

    @staticmethod
    def create(entry, translation):
        return Example(id=uuid.uuid4(), object=entry, subject=translation)
