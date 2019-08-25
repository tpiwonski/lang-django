from django.core.exceptions import ObjectDoesNotExist
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
        return self.prefetch_related(
            models.Prefetch('related_objects'),
            models.Prefetch('related_subjects')
        )


class EntryManager(models.Manager):
    
    def get_queryset(self):
        return EntryQuerySet(self.model, using=self._db)

    def save(self, entry):
        pass

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

    def delete_entry(self, entry_id):
        self.get_queryset().filter(id=entry_id).delete()


class EntryModel(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=255)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    objects = EntryManager()

    class Meta:
        db_table = 'dictionary_entry'
        unique_together = (('text', 'language'),)

    @property
    def translated_entries(self):
        from lang.dictionary.models import Entry
        return Entry.objects.filter(Q(related_subjects__subject=self) | Q(related_objects__object=self))

    @property
    def translations(self):
        from lang.dictionary.models import Translation
        return Translation.objects.filter(Q(subject=self) | Q(object=self))

    def get_examples(self, entry):
        from lang.dictionary.models import Example
        return Example.objects.filter(
            (Q(example_translations__translation__object=entry) & Q(example_translations__translation__subject=self)) |
            (Q(example_translations__translation__object=self) & Q(example_translations__translation__subject=entry)))

    def get_translation(self, entry):
        from lang.dictionary.models import Translation
        return Translation.objects.filter(
            (Q(object=self) & Q(subject=entry)) | (Q(object=entry) & Q(subject=self))).first()

    def has_translation(self, entry):
        from lang.dictionary.models import Translation
        return Translation.objects.filter(
            (Q(object=self) & Q(subject=entry)) | (Q(object=entry) & Q(subject=self))).exists()
