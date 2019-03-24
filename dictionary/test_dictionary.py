import pytest

# from dictionary.application import AddWord
# from dictionary.repositories import WordRepository


# @pytest.fixture
# def word_repository():
#     return WordRepository


# @pytest.fixture
# def add_word():
#     return AddWord()


# @pytest.mark.django_db
# def test_add_word(add_word: AddWord, word_repository: WordRepository):
#     expected_word = add_word.execute(word="test", language="pl")

#     actual_word = word_repository.get_word_by_id(word_id=expected_word.id)

#     assert actual_word.id == expected_word.id
#     assert actual_word.word == expected_word.word
