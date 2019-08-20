from django.contrib import admin

# Register your models here.

from lang.dictionary.models import Entry, Relation, RelationExample, Example

admin.site.register(Entry)
admin.site.register(Relation)
admin.site.register(RelationExample)
admin.site.register(Example)
