from rest_framework.serializers import Serializer, CharField, ChoiceField, UUIDField, ModelSerializer, SerializerMethodField

from lang.dictionary.models import Entry, LANGUAGES, Translation, Example
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


class TranslationEntryOutput(ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'text', 'language']


class TranslationExampleOutput(ModelSerializer):
    object = TranslationEntryOutput()
    subject = TranslationEntryOutput()

    class Meta:
        model = Example
        fields = ['id', 'object', 'subject']


class EntryTranslationOutput(Serializer):
    entry = TranslationEntryOutput()
    examples = TranslationExampleOutput(many=True)


class EntryRecordingOutput(ModelSerializer):

    class Meta:
        model = EntryRecordingData
        fields = ['id', 'url']


class EntryOutput(ModelSerializer):
    foo_translations = EntryTranslationOutput(many=True)
    translations = TranslationOutput(many=True)
    # examples = EntryExampleOutput(many=True)
    recordings = EntryRecordingOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'foo_translations', 'translations', 'recordings'] #, 'examples']


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
