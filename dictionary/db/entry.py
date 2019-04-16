import uuid

from django.db import models
from django.db.models.expressions import Q

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

    def save(self, entry): # TODO is this method really needed?
        entry.save()
        for translation in entry._translations:
            translation.translated.save()
            translation.save()

    def get_by_id(self, entry_id):
        try:
            return self.get_queryset().with_translations().get(id=entry_id)
        except models.ObjectDoesNotExist:
            return None

    def get_all(self):
        return self.get_queryset().with_translations().order_by('text').all()

    def find(self, text, language=None):
        qs = self.get_queryset().filter(text__icontains=text).order_by('text')
        if language:
            qs = qs.filter(language=language)

        return qs.with_translations()

    # def get_all_by_id(self, word_ids):
    #     return self.get_queryset().filter(id__in=word_ids).with_translations()

    # def get_translations(self, word):
    #     return [t.source if t.translated == word else t.translation 
    #             for t in word.source.all().union(word.translated.all())]


class EntryData(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=255)
    language = models.CharField(max_length=2, choices=LANGUAGES)

    objects = EntryManager()

    class Meta:
        db_table = 'dictionary_entry'
        unique_together = (('text', 'language'),)
    
    def __init__(self, *args, **kwargs):
        super(EntryData, self).__init__(*args, **kwargs)

        self._translations = []

    @property
    def translations(self):
        return ([t.translated for t in self.source.all()] + 
                [t.source for t in self.translated.all()])

    def _add_translation(self, translation):
        self._translations.append(translation)
