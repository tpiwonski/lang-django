from django.db import models


class TranslationExampleModel(models.Model):
    id = models.UUIDField(primary_key=True)
    translation = models.ForeignKey('lang.Translation', on_delete=models.CASCADE, related_name='translation_examples')
    example = models.ForeignKey('lang.Example', on_delete=models.CASCADE, related_name='example_translations')

    class Meta:
        db_table = 'dictionary_translation_example'
