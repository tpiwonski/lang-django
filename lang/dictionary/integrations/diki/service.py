from lang.dictionary.db.entry import ENTRY_TYPE_NOUN, ENTRY_TYPE_ADVERB, ENTRY_TYPE_ADJECTIVE, ENTRY_TYPE_VERB, \
    ENTRY_TYPE_PRONOUN, ENTRY_TYPE_PREPOSITION, ENTRY_TYPE_CONJUNCTION, ENTRY_TYPE_INTERJECTION, ENTRY_TYPE_IDIOM, \
    ENTRY_TYPE_PHRASAL_VERB, ENTRY_TYPE_PREFIX, ENTRY_TYPE_UNKNOWN
from .client import HtmlClient

ENTRY_TYPES_MAP = {
    None: ENTRY_TYPE_UNKNOWN,
    'rzeczownik': ENTRY_TYPE_NOUN,
    'przysłówek': ENTRY_TYPE_ADVERB,
    'przymiotnik': ENTRY_TYPE_ADJECTIVE,
    'czasownik': ENTRY_TYPE_VERB,
    'zaimek': ENTRY_TYPE_PRONOUN,
    'przyimek': ENTRY_TYPE_PREPOSITION,
    'spójnik': ENTRY_TYPE_CONJUNCTION,
    'wykrzyknik': ENTRY_TYPE_INTERJECTION,
    'idiom': ENTRY_TYPE_IDIOM,
    'phrasal verb': ENTRY_TYPE_PHRASAL_VERB,
    'prefiks': ENTRY_TYPE_PREFIX,
    # 'phrase': ENTRY_TYPE_PHRASE = 12
    # 'sentenceENTRY_TYPE_SENTENCE = 13
}


class TranslationService(object):

    def __init__(self):
        self.client = HtmlClient()

    def translate(self, text: str):
        result = self.client.translate(text)
        if not result:
            return []

        entry_language, translation_language = result['dictionary']
        entries_by_type = {}
        for entry in result['entries']:
            translations = []
            for meaning in entry['meanings']:

                et = ENTRY_TYPES_MAP.get(meaning.get('part_of_speech'), ENTRY_TYPE_UNKNOWN)
                e = entries_by_type.setdefault((et, entry['text']), {
                    'text': entry['text'],
                    'language': entry_language,
                    'type': et,
                    'translations': [],
                    'recordings': entry['recordings']
                })

                e['translations'].append({
                    'entries': meaning['translations'],
                    'language': translation_language,
                    'recordings': meaning['recordings'],
                    'examples': meaning['examples'],
                    'type': et
                })

            # entries.append({
            #     'text': entry['text'],
            #     'language': entry_language,
            #     'translations': translations,
            #     'recordings': entry['recordings']
            # })

        return entries_by_type.values()
