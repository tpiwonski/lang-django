from django.db import models


class TranslationModel(models.Model):
    id = models.UUIDField(primary_key=True)
    object = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='related_subjects')
    subject = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='related_objects')

    class Meta:
        db_table = 'dictionary_translation'
        unique_together = (('object', 'subject'),)

    def __init__(self, *args, **kwargs):
        super(TranslationModel, self).__init__(*args, **kwargs)

        self._add_examples = []
        self._remove_examples = []

    def get_example(self, example):
        translation_example = [e for e in self.translation_examples.all() if e.example == example]
        if translation_example:
            return translation_example[0]

        return None

    def add_example(self, example):
        from lang.dictionary.models import TranslationExample

        translation_example = TranslationExample.create(translation=self, example=example)
        self._add_examples.append(translation_example)
        return translation_example
