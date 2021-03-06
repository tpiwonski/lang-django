from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q

from lang.dictionary.db.entry import ENTRY_TYPE_SENTENCE


class ExampleManager(models.Manager):

    def get_by_text(self, text):
        try:
            return self.get_queryset().get(
                (Q(object__text=text) & Q(object__type=ENTRY_TYPE_SENTENCE)) |
                (Q(subject__text=text) & Q(subject__type=ENTRY_TYPE_SENTENCE)))
        except ObjectDoesNotExist:
            return None


class ExampleModel(models.Model):
    id = models.UUIDField(primary_key=True)
    object = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='example_subjects')
    subject = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='example_objects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ExampleManager()

    class Meta:
        db_table = 'dictionary_example'
