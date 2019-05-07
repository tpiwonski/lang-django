from django.db import models

from lang.models import Entry


class RepetitionManager(models.Manager):
    pass


class RepetitionData(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    objects = RepetitionManager()

    class Meta:
        db_table = 'repetition'

    def __init__(self, *args, **kwargs):
        super(RepetitionData, self).__init__(*args, **kwargs)

        self._repeated_entries = []


class RepeatedEntryData(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    repetition = models.ForeignKey('lang.Repetition', on_delete=models.CASCADE, related_name='repeated_entries')
    entry = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='repeated_entries')

    class Meta:
        db_table = 'repeated_entry'
