import uuid

from lang.dictionary.db.recording import RecordingModel


class Recording(RecordingModel):

    class Meta:
        proxy = True

    @classmethod
    def create(cls, entry, audio_url):
        return Recording.objects.create(id=uuid.uuid4(), entry=entry, audio_url=audio_url)
