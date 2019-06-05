from rest_framework.serializers import Serializer, CharField, ChoiceField, UUIDField, ModelSerializer, SerializerMethodField

from lang.dictionary.models import Entry, LANGUAGES, Relation
from lang.dictionary.db.entry import EntryRecordingData


class EntryInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class ExampleTranslationOutput(ModelSerializer):

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language']


class EntryExampleOutput(ModelSerializer):
    translations = ExampleTranslationOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'translations']


class TranslationOutput(ModelSerializer):
    # examples = EntryExampleOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language'] #, 'examples']


class EntryRecordingOutput(ModelSerializer):

    class Meta:
        model = EntryRecordingData
        fields = ['id', 'url']


class EntryOutput(ModelSerializer):
    translations = TranslationOutput(many=True)
    # examples = EntryExampleOutput(many=True)
    recordings = EntryRecordingOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'translations', 'recordings'] #, 'examples']


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
