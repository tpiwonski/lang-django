import uuid

from django.db import models

from dictionary.repositories.word import WordManager


LANGUAGE_PL = 'pl'
LANGUAGE_EN = 'en'

LANGUAGES = (
    (LANGUAGE_PL, u'Polish'),
    (LANGUAGE_EN, u'English')
)


class Word(models.Model):
    id = models.UUIDField(primary_key=True)
    word = models.CharField(max_length=255)
    language = models.CharField(max_length=2, choices=LANGUAGES)

    objects = WordManager()

    class Meta:
        db_table = 'dictionary_word'
        unique_together = (('word', 'language'),)
    
    def __init__(self, *args, **kwargs):
        super(Word, self).__init__(*args, **kwargs)

        self._translations = []

    @staticmethod
    def create(word, language):
        return Word(id=uuid.uuid4(), word=word, language=language)

    @property
    def translations(self):
        return ([t.translated for t in self.source.all()] + 
                [t.source for t in self.translated.all()])

    def add_translation(self, translated_word):
        if self.has_translation(translated_word):
            return

        translation = Translation.create(source=self, translated=translated_word)
        self._translations.append(translation)

    def has_translation(self, translated_word):
        return any([t for t in self.translations 
                    if t.word == translated_word.word and t.language == translated_word.language])


class Translation(models.Model):
    id = models.UUIDField(primary_key=True)
    source = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='source')
    translated = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='translated')

    class Meta:
        db_table = 'dictionary_translation'
        unique_together = (('source', 'translated'),)

    @staticmethod
    def create(source, translated):
        return Translation(id=uuid.uuid4(), source=source, translated=translated)
