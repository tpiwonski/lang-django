from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.expressions import Q

LANGUAGE_PL = 'pl'
LANGUAGE_EN = 'en'

LANGUAGES = (
    (LANGUAGE_PL, u'Polish'),
    (LANGUAGE_EN, u'English')
)


ENTRY_TYPE_UNKNOWN = 0
ENTRY_TYPE_NOUN = 1
ENTRY_TYPE_ADVERB = 2
ENTRY_TYPE_ADJECTIVE = 3
ENTRY_TYPE_PRONOUN = 4
ENTRY_TYPE_VERB = 5
ENTRY_TYPE_PREPOSITION = 6
ENTRY_TYPE_CONJUNCTION = 7
ENTRY_TYPE_INTERJECTION = 8
ENTRY_TYPE_IDIOM = 9
ENTRY_TYPE_PHRASAL_VERB = 10
ENTRY_TYPE_PREFIX = 11
ENTRY_TYPE_PHRASE = 12
ENTRY_TYPE_SENTENCE = 13

ENTRY_TYPES = (
    (ENTRY_TYPE_UNKNOWN, 'unknown'),
    (ENTRY_TYPE_NOUN, 'noun'),
    (ENTRY_TYPE_ADVERB, 'adverb'),
    (ENTRY_TYPE_ADJECTIVE, 'adjective'),
    (ENTRY_TYPE_VERB, 'verb'),
    (ENTRY_TYPE_PRONOUN, 'pronoun'),
    (ENTRY_TYPE_PREPOSITION, 'preposition'),
    (ENTRY_TYPE_CONJUNCTION, 'conjunction'),
    (ENTRY_TYPE_INTERJECTION, 'interjection'),
    (ENTRY_TYPE_IDIOM, 'idiom'),
    (ENTRY_TYPE_PHRASAL_VERB, 'phrasal verb'),
    (ENTRY_TYPE_PREFIX, 'prefix'),
    (ENTRY_TYPE_PHRASE, 'phrase'),
    (ENTRY_TYPE_SENTENCE, 'sentence'),
)


class EntryQuerySet(models.QuerySet):

    def with_translations(self):
        return self.prefetch_related(
            models.Prefetch('translation_objects'),
            models.Prefetch('translation_subjects')
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

    def get_by_text(self, text, language, entry_type):
        try:
            return self.get_queryset().with_translations().get(text=text, language=language, type=entry_type)
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
    type = models.PositiveSmallIntegerField(choices=ENTRY_TYPES, default=0)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    objects = EntryManager()

    class Meta:
        db_table = 'dictionary_entry'
        unique_together = (('text', 'language', 'type'),)

    @property
    def translated_entries(self):
        from lang.dictionary.models import Entry
        return Entry.objects.filter(Q(translation_subjects__subject=self) | Q(translation_objects__object=self))

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
            ((Q(object=self) & Q(subject=entry)) | (Q(object=entry) & Q(subject=self)))).first()

    def has_translation(self, entry):
        from lang.dictionary.models import Translation
        return Translation.objects.filter(
            (Q(object=self) & Q(subject=entry)) | (Q(object=entry) & Q(subject=self))).exists()

    def has_recording(self, url):
        from lang.dictionary.models import Recording
        return Recording.objects.filter(entry=self, url=url).exists()

    def has_synonym(self, entry):
        from lang.dictionary.models import Synonym
        return Synonym.objects.filter(
            (Q(object=self) & Q(subject=entry)) | (Q(object=entry) & Q(subject=self))).exists()

    @property
    def synonyms(self):
        from lang.dictionary.models import Entry
        return Entry.objects.filter(Q(synonym_subjects__subject=self) | Q(synonym_objects__object=self)).distinct()
