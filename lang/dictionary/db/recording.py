from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class RecordingManager(models.Manager):

    def get_by_url(self, url):
        try:
            return self.get_queryset().get(url=url)
        except ObjectDoesNotExist as ex:
            return None


class RecordingModel(models.Model):
    id = models.UUIDField(primary_key=True)
    entry = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='recordings')
    audio_url = models.URLField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RecordingManager()

    class Meta:
        db_table = 'dictionary_recording'
