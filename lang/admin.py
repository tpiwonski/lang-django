from django.contrib import admin

# Register your models here.

from lang.dictionary.models import Entry, Translation, TranslationExample, Example

admin.site.register(Entry)
admin.site.register(Translation)
admin.site.register(TranslationExample)
admin.site.register(Example)
