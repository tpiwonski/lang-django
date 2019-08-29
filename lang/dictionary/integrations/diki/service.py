from lang.dictionary.db.entry import POS_CONJUNCTION, POS_PREPOSITION, POS_PRONOUN, POS_VERB, POS_ADJECTIVE, POS_ADVERB, \
    POS_NOUN
from .client import HtmlClient

PARTS_OF_SPEECH_PL = {
    'rzeczownik': POS_NOUN,
    'przysłówek': POS_ADVERB,
    'przymiotnik': POS_ADJECTIVE,
    'czasownik': POS_VERB,
    'zaimek': POS_PRONOUN,
    'przyimek': POS_PREPOSITION,
    'spójnik': POS_CONJUNCTION
}


class TranslationService(object):

    def __init__(self):
        self.client = HtmlClient()

    def translate(self, text: str):
        result = self.client.translate(text)
        if not result:
            return []

        entry_language, translation_language = result['dictionary']
        entries = []
        for entry in result['entries']:
            translations = []
            for meaning in entry['meanings']:
                translations.append({
                    'entries': meaning['translations'],
                    'language': translation_language,
                    'recordings': meaning['recordings'],
                    'examples': meaning['examples'],
                    'part_of_speech': PARTS_OF_SPEECH_PL.get(meaning.get('part_of_speech'))
                })

            entries.append({
                'text': entry['text'],
                'language': entry_language,
                'translations': translations,
                'recordings': entry['recordings']
            })

        return entries
