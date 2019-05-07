import uuid

from django.db import models
from django.db.models.expressions import Q
from django.core.exceptions import ObjectDoesNotExist

from lang.dictionary.db.translation import TranslationData


LANGUAGE_PL = 'pl'
LANGUAGE_EN = 'en'

LANGUAGES = (
    (LANGUAGE_PL, u'Polish'),
    (LANGUAGE_EN, u'English')
)


class EntryQuerySet(models.QuerySet):
    def with_translations(self):
        # from dictionary.models import Translation

        return self.prefetch_related(
            models.Prefetch('source'), 
            models.Prefetch('translated')
        )
 
        # return self.annotate(translation_ids=models.Subquery(
        #     self.model.objects.filter(
        #         Q(source__translated_id=models.OuterRef('pk')) | 
        #         Q(translated__source_id=models.OuterRef('pk'))
        #     ).values('id'),
        #     output_field=models.QuerySet()
        # ))
        
        # return self.model.objects.prefetch_related(models.Prefetch(''))


class EntryManager(models.Manager):
    
    def get_queryset(self):
        return EntryQuerySet(self.model, using=self._db)

    def save(self, entry):
        from lang.dictionary.models.translation import Translation

        q = Q()
        for translation in entry._remove_translations:
            q |= Q(source=entry, translated=translation) | Q(source=translation, translated=entry)

        if q:
            Translation.objects.filter(q).delete()

        entry.save()
        for translation in entry.translations:
            translation.save()
        
        for recording in entry._add_recordings:
            recording.save()

        for translation in entry._add_translations:
            translation.save()
            Translation.create(source=entry, translated=translation).save()

        entry._add_translations = []
        entry._add_recordings = []
        entry._remove_translations = []

    def delete(self, entry_id):
        self.get_queryset().filter(id=entry_id).delete()

    def get_by_id(self, entry_id):
        try:
            return self.get_queryset().with_translations().get(id=entry_id)
        except ObjectDoesNotExist as ex:
            return None

    def get_by_text(self, text, language):
        try:
            return self.get_queryset().with_translations().get(text=text, language=language)
        except ObjectDoesNotExist as ex:
            return None

    def get_all(self):
        return self.get_queryset().with_translations().order_by('text').all()

    def search_with_text(self, text, language=None):
        qs = self.get_queryset().with_translations().filter(text__icontains=text) 
        if language:
            qs = qs.filter(language=language)

        return qs.order_by('text')


class EntryData(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=255)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    objects = EntryManager()

    class Meta:
        db_table = 'dictionary_entry'
        unique_together = (('text', 'language'),)
    
    def __init__(self, *args, **kwargs):
        super(EntryData, self).__init__(*args, **kwargs)

        self._add_translations = []
        self._remove_translations = []
        self._add_recordings = []

    @property
    def translations(self):
        return ([t.translated for t in self.source.all()] + 
                [t.source for t in self.translated.all()] +
                self._add_translations)

    def add_translation(self, entry):
        self._add_translations.append(entry)

    def remove_translation(self, entry):
        self._remove_translations.append(entry)

    def add_recording(self, recording):
        self._add_recordings.append(recording)


class EntryRecordingData(models.Model):
    id = models.UUIDField(primary_key=True)
    entry = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='recordings')
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'dictionary_entry_recording'
