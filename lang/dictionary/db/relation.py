from django.db import models

RELATION_KIND_TRANSLATION = 1
RELATION_KIND_SYNONYM = 2

RELATION_KINDS = (
    (RELATION_KIND_TRANSLATION, 'Translation'),
    (RELATION_KIND_SYNONYM, 'Synonym'),
)


class RelationData(models.Model):
    id = models.UUIDField(primary_key=True)
    object = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='related_subjects')
    subject = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='related_objects')
    kind = models.IntegerField(choices=RELATION_KINDS)

    class Meta:
        db_table = 'dictionary_relation'
        unique_together = (('object', 'subject', 'kind'),)

    def __init__(self, *args, **kwargs):
        super(RelationData, self).__init__(*args, **kwargs)

        self._add_examples = []
        self._remove_examples = []

    def get_example(self, example):
        relation_example = [e for e in self.relation_examples.all() if e.example == example]
        if relation_example:
            return relation_example[0]

        return None

    def add_example(self, example):
        from lang.dictionary.models import RelationExample

        relation_example = RelationExample.create(relation=self, example=example)
        self._add_examples.append(relation_example)
        return relation_example
