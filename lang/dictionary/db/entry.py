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
        # from dictionary.models import Translation

        return self.prefetch_related(
            models.Prefetch('related_objects'),
            models.Prefetch('related_subjects')
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
            q |= Q(object=entry, subject=translation) | Q(object=translation, subject=entry)

        if q:
            Translation.objects.filter(q).delete()

        entry.save()
        for translation in entry.translations:
            translation.save()
        
        for recording in entry._add_recordings:
            recording.save()

        for translation in entry._add_translations:
            translation.save()
            for example in translation._add_examples:
                self.save(example.example.object)
                self.save(example.example.subject)
                # example.example.object.save()
                # example.example.subject.save()
                example.example.save()
                example.save()

            # Translation.create(source=entry, translated=translation).save()

        # for example in entry._add_examples:
        #     example.save()
            # Example.create(entry=entry, example=example).save()

        entry._add_translations = []
        entry._add_examples = []
        entry._add_recordings = []
        # entry._remove_examples = []
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

    # def delete_entry_with_translations(self, entry_id):
    #     self.get_queryset().filter(Q(source__translated_id=entry_id) | Q(translated__source_id=entry_id)).delete()
    #     self.get_queryset().filter(id=entry_id).delete()

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
    
    def __init__(self, *args, **kwargs):
        super(EntryModel, self).__init__(*args, **kwargs)

        self._add_translations = []
        self._remove_translations = []
        self._add_recordings = []
        # self._add_examples = []
        # self._remove_examples = []

    @property
    def translations(self):
        return ([t.subject for t in self.related_subjects.all()] +
                [t.object for t in self.related_objects.all()] +
                [t.subject for t in self._add_translations])

    def get_examples(self, entry):
        translations = ([t for t in self.related_subjects.filter(subject=entry)] +
                        [t for t in self.related_objects.filter(object=entry)] +
                        [t for t in self._add_translations if t.subject == entry])

        examples = set()
        for t in translations:
            examples.update((e.example for e in t.translation_examples.all()))

        return examples

    def get_translation(self, entry):
        translations = ([t for t in self.related_subjects.all() if t.subject == entry] +
                        [t for t in self.related_objects.all() if t.object == entry] +
                        [t for t in self._add_translations if t.subject == entry])
        if translations:
            return translations[0]

        return None

    def add_translation(self, entry):
        from lang.dictionary.models.translation import Translation
        translation = Translation.create(object=self, subject=entry)
        self._add_translations.append(translation)
        return translation

    def remove_translation(self, entry):
        self._remove_translations.append(entry)

    # def get_examples(self, relation):
    #     self.entry_examples.filter(relation=relation).all()
    #
    # def add_example(self, relation, text, translation):
    #     # if self.has_example(entry):
    #     #     raise Exception("Example already exists")
    #
    #     from lang.dictionary.models import Example
    #     self._add_examples.append(Example.create(relation=relation, text=text, translation=translation))

    # def has_example(self, entry):
    #     return any([e for e in self.examples
    #                 if e.text == entry.text and e.language == entry.language])

    def add_recording(self, recording):
        self._add_recordings.append(recording)


class EntryRecordingData(models.Model):
    id = models.UUIDField(primary_key=True)
    entry = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='recordings')
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'dictionary_entry_recording'
