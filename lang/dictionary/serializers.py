from dataclasses import dataclass
from typing import List

from rest_framework.serializers import Serializer, CharField, ChoiceField, ModelSerializer, SerializerMethodField

from lang.dictionary.db.entry import LANGUAGES
from lang.dictionary.models import Example, Entry, Recording


class EntryInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class TranslationOutput(ModelSerializer):

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'type', 'source_url']


class RecordingOutput(ModelSerializer):

    class Meta:
        model = Recording
        fields = ['audio_url']


class TranslationEntryOutput(ModelSerializer):
    recordings = RecordingOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'source_url', 'recordings']


class TranslationExampleOutput(ModelSerializer):
    object = TranslationEntryOutput()
    subject = TranslationEntryOutput()

    class Meta:
        model = Example
        fields = ['id', 'object', 'subject']


class EntryTranslationOutput(Serializer):
    entry = TranslationEntryOutput()
    examples = TranslationExampleOutput(many=True)


class SynonymOutput(ModelSerializer):

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language']


class ViewEntryOutput(ModelSerializer):
    translations = SerializerMethodField()
    translated_entries = TranslationOutput(many=True)
    recordings = RecordingOutput(many=True)
    synonyms = SynonymOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'source_url', 'translations', 'translated_entries', 'recordings', 'synonyms']

    def get_translations(self, entry):
        result = [EntryTranslation(t.subject if t.object == entry else t.object, t.examples)
                  for t in entry.translations]
        return EntryTranslationOutput(result, many=True).data


class EditEntryOutput(ModelSerializer):
    translated_entries = TranslationOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'type', 'translated_entries']


@dataclass
class EntryTranslation:
    entry: Entry
    examples: List[int]


class TranslationInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class AddTranslationInput(Serializer):
    entry = EntryInput()
    translations = TranslationInput(many=True)
