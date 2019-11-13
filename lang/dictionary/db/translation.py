from django.db import models


class TranslationModel(models.Model):
    id = models.UUIDField(primary_key=True)
    object = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='translation_subjects')
    subject = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='translation_objects')
    usage_notes = models.CharField(max_length=256, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dictionary_translation'
        unique_together = (('object', 'subject'),)

    @property
    def examples(self):
        from lang.dictionary.models import Example
        return Example.objects.filter(example_translations__translation=self).all()

    @property
    def usage_notes_list(self):
        return self.usage_notes.split(',') if self.usage_notes else []

    def has_example(self, example):
        return self.translation_examples.filter(example=example).exists()
