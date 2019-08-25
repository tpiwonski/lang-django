from django.db import models


class TranslationModel(models.Model):
    id = models.UUIDField(primary_key=True)
    object = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='related_subjects')
    subject = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='related_objects')

    class Meta:
        db_table = 'dictionary_translation'
        unique_together = (('object', 'subject'),)

    @property
    def examples(self):
        from lang.dictionary.models import Example
        return Example.objects.filter(example_translations__translation=self).all()

    def has_example(self, example):
        return self.translation_examples.filter(example=example).exists()
