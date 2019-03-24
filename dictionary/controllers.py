import uuid

from dictionary.models import Word, Translation
from dictionary.data import FindByWordData, WordData, GetWordsData


class AddWord(object):
    word_repository = Word.objects

    def execute(self, word, language) -> Word:
        word = Word(id=uuid.uuid4(), word=word, language=language)
        self.word_repository.save(word)
        return word


class GetAllWords(object):
    word_repository = Word.objects

    def execute(self):
        words = self.word_repository.get_all()
        return GetWordsData(
            results=[WordData(word=word) for word in words]
        )


class FindByWord(object):
    word_repository = Word.objects

    def execute(self, word):
        words = self.word_repository.find_by_word(word)
        return FindByWordData(
            results=[WordData(word=word) for word in words]
        )


class AddTranslation(object):
    word_repository = Word.objects

    def execute(self, source_word_id, translated_word_id):
        source_word = self.word_repository.get_by_id(source_word_id)
        translated_word = self.word_repository.get_by_id(translated_word_id)
        translation = Translation(id=uuid.uuid4(), source=source_word, translated=translated_word)
        translation.save() # TODO better way?
        # self.word_manager.save(source_word)
        return translation
