import uuid

from django.db import models
from django.db.models.expressions import Q

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

    def save(self, entry): # TODO is this method really needed?
        from lang.dictionary.models.translation import Translation

        entry.save()
        for translation in entry.translations:
            translation.save()
        
        for translation in entry._add_translations:
            translation.save()
            Translation.create(source=entry, translated=translation).save()

        q = Q()
        for translation in entry._remove_translations:
            q |= Q(source=entry, translated=translation) | Q(source=translation, translated=entry)

        if q:
            Translation.objects.filter(q).delete()

        # for translation in entry._translations:
        #     translation.translated.save()
        #     translation.save()

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

    @property
    def translations(self):
        return ([t.translated for t in self.source.all()] + 
                [t.source for t in self.translated.all()])

    def add_translation(self, entry):
        self._add_translations.append(entry)

    #     from lang.dictionary.models.translation import Translation
    #     translation = Translation.create(source=self, translated=entry)
    #     translation.save()

    #     # self._translations.append(translation)

    def remove_translation(self, entry):
        self._remove_translations.append(entry)

    #     from lang.dictionary.models.translation import Translation
    #     Translation.objects.filter(
    #         Q(source=self, translated=entry) | 
    #         Q(source=entry, translated=self)).delete()

    #     # self._removed_translations.append(entry)
