import uuid

from django.db import models
from django.db.models.expressions import Q


class WordQuerySet(models.QuerySet):
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


class WordManager(models.Manager):
    
    def get_queryset(self):
        return WordQuerySet(self.model, using=self._db)

    def save(self, word): # TODO is this method really needed?
        word.save()
        for translation in word._translations:
            translation.translated.save()
            translation.save()

    def get_by_id(self, word_id):
        try:
            return self.get_queryset().with_translations().get(id=word_id)
        except models.ObjectDoesNotExist:
            return None

    def get_all(self):
        return self.get_queryset().with_translations().all()

    def find_with_word(self, word):
        return self.get_queryset().filter(word__icontains=word).with_translations()

    def find_word(self, word, language):
        return self.get_queryset().filter(word__iexact=word, language=language).with_translations()

    def get_all_by_id(self, word_ids):
        return self.get_queryset().filter(id__in=word_ids).with_translations()

    # def get_translations(self, word):
    #     return [t.source if t.translated == word else t.translation 
    #             for t in word.source.all().union(word.translated.all())]
