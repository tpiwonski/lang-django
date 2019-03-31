import uuid

from rest_framework.serializers import Serializer, CharField, ChoiceField, UUIDField
from dictionary.models import Word, LANGUAGES


class WordInput(Serializer):
    word = CharField()
    language = ChoiceField(choices=LANGUAGES)


class TranslatedWordOutput(Serializer):
    id = UUIDField()
    word = CharField()
    language = ChoiceField(choices=LANGUAGES)


class WordOutput(Serializer):
    id = UUIDField()
    word = CharField()
    language = ChoiceField(choices=LANGUAGES)
    translations = TranslatedWordOutput(many=True)


class TranslationInput(Serializer):
    word = CharField()
    language = ChoiceField(choices=LANGUAGES)


class AddTranslationInput(Serializer):
    word = WordInput()
    translations = TranslationInput(many=True)


class AddTranslationOutput(Serializer):
    id = UUIDField()


class AddWord(object):
    word_repository = Word.objects

    def execute(self, word, language) -> Word:
        word = Word.create(word=word, language=language)
        self.word_repository.save(word)
        return WordOutput(word).data


class GetAllWords(object):
    word_repository = Word.objects

    def execute(self):
        words = self.word_repository.get_all()
        return [WordOutput(word).data for word in words]


class FindWord(object):
    word_repository = Word.objects

    def execute(self, word):
        words = self.word_repository.find_word(word)
        return [WordOutput(word).data for word in words]


class AddTranslation(object):
    word_repository = Word.objects

    def execute(self, word, translations):
        source_word = self.word_repository.find_word(word['word'], word['language'])
        if source_word:
            source_word = source_word[0]
        else:
            source_word = Word.create(word['word'], word['language'])

        for translation in translations:
            translated_word = self.word_repository.find_word(translation['word'], translation['language'])
            if translated_word:
                translated_word = translated_word[0]
            else:
                translated_word = Word.create(translation['word'], translation['language'])

            if not source_word.has_translation(translated_word):
                source_word.add_translation(translated_word)

        self.word_repository.save(source_word)
        return AddTranslationOutput(source_word).data
