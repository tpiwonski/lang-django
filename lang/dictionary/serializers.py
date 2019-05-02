from rest_framework.serializers import Serializer, CharField, ChoiceField, UUIDField, ModelSerializer, SerializerMethodField

from lang.dictionary.models import Entry, LANGUAGES, Translation


class EntryInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class TranslationOutput(ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'text', 'language']


class EntryOutput(ModelSerializer):
    translations = TranslationOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'translations']


class TranslationInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class AddTranslationInput(Serializer):
    entry = EntryInput()
    translations = TranslationInput(many=True)


class AddEntryOutput(ModelSerializer):
    
    class Meta:
        model = Entry
        fields = ['id']
