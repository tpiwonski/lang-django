from django.db import models

from lang.dictionary.db.entry import PARTS_OF_SPEECH


class PartOfSpeech(models.Model):
    id = models.UUIDField(primary_key=True)
    entry = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='parts_of_speech')
    part_of_speech = models.CharField(max_length=2, choices=PARTS_OF_SPEECH)
    
    class Meta:
        db_table = 'part_of_speech'
        unique_together = (('entry', 'part_of_speech'),)
