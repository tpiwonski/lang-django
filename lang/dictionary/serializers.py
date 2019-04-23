from rest_framework.serializers import Serializer, CharField, ChoiceField, UUIDField, ModelSerializer, SerializerMethodField

from lang.dictionary.models import Entry, LANGUAGES, Translation


class EntryInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class TranslatedEntryOutput(ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'text', 'language']


class EntryOutput(ModelSerializer):
    translations = TranslatedEntryOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'translations']


class TranslationInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class AddTranslationInput(Serializer):
    entry = EntryInput()
    translations = TranslationInput(many=True)


class AddTranslationOutput(ModelSerializer):
    
    class Meta:
        model = Entry
        fields = ['id']
