from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q


class ExampleManager(models.Manager):

    def get_by_text(self, text):
        try:
            return self.get_queryset().get(Q(object__text=text) | Q(subject__text=text))
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
    # text = models.CharField(max_length=255)
    # translation = models.CharField(max_length=255)
    object = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='example_subjects')
    subject = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='example_objects')

    objects = ExampleManager()

    class Meta:
        db_table = 'dictionary_example'
