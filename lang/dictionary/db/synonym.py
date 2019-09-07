from django.db import models


class SynonymModel(models.Model):
    id = models.UUIDField(primary_key=True)
    object = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='synonym_subjects')
    subject = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='synonym_objects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dictionary_synonym'
        unique_together = (('object', 'subject'),)
