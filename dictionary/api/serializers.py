from rest_framework.serializers import Serializer, CharField, ChoiceField, UUIDField

from dictionary.models import LANGUAGES


class AddWordSerializer(Serializer):
    word = CharField()
    language = ChoiceField(choices=LANGUAGES)


class TranslationSerializer(Serializer):
    id = UUIDField()


class TranslatedWordSerializer(Serializer):
    id = UUIDField()
    word = CharField()
    language = ChoiceField(choices=LANGUAGES)


class WordSerializer(Serializer):
    id = UUIDField()
    word = CharField()
    language = ChoiceField(choices=LANGUAGES)
    translations = TranslatedWordSerializer(many=True)


class WordDataSerializer(Serializer):
    word = WordSerializer()


class FindByWordSerializer(Serializer):
    results = WordDataSerializer(many=True)


class GetWordsSerializer(Serializer):
    results = WordDataSerializer(many=True)


class AddTranslationSerializer(Serializer):
    source_word_id = UUIDField()
    translated_word_id = UUIDField()
