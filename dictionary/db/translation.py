from django.db import models


class TranslationData(models.Model):
    id = models.UUIDField(primary_key=True)
    source = models.ForeignKey('dictionary.Entry', on_delete=models.CASCADE, related_name='source')
    translated = models.ForeignKey('dictionary.Entry', on_delete=models.CASCADE, related_name='translated')

    class Meta:
        db_table = 'dictionary_translation'
        unique_together = (('source', 'translated'),)
