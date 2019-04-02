import uuid

from django.db import models


class Translation(models.Model):
    id = models.UUIDField(primary_key=True)
    source = models.ForeignKey('dictionary.Entry', on_delete=models.CASCADE, related_name='source')
    translated = models.ForeignKey('dictionary.Entry', on_delete=models.CASCADE, related_name='translated')

    class Meta:
        db_table = 'dictionary_translation'
        unique_together = (('source', 'translated'),)

    @staticmethod
    def create(source, translated):
        return Translation(id=uuid.uuid4(), source=source, translated=translated)
