from django.db import models


class ExampleData(models.Model):
    id = models.UUIDField(primary_key=True)
    entry = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='entry_examples')
    example = models.ForeignKey('lang.Entry', on_delete=models.CASCADE, related_name='example_entries')

    class Meta:
        db_table = 'dictionary_example'
        unique_together = (('entry', 'example'),)
