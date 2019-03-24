from django.db import models

from dictionary.repositories import WordManager


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
    
    @property
    def translations(self):
        return ([t.translated for t in self.source.all()] + 
                [t.source for t in self.translated.all()])


class Translation(models.Model):
    id = models.UUIDField(primary_key=True)
    source = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='source')
    translated = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='translated')

    class Meta:
        db_table = 'dictionary_translation'
        unique_together = (('source', 'translated'),)
