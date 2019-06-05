from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ExampleManager(models.Manager):

    def get_by_text(self, text):
        try:
            return self.get_queryset().get(text=text)
        except ObjectDoesNotExist:
            return None


class RelationExampleData(models.Model):
    id = models.UUIDField(primary_key=True)
    relation = models.ForeignKey('lang.Relation', on_delete=models.CASCADE, related_name='relation_examples')
    example = models.ForeignKey('lang.Example', on_delete=models.CASCADE, related_name='example_relations')

    class Meta:
        db_table = 'dictionary_relation_example'


class ExampleData(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)

    objects = ExampleManager()

    class Meta:
        db_table = 'dictionary_example'
