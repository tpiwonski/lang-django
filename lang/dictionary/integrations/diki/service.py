from lang.dictionary.db.entry import ENTRY_TYPE_NOUN, ENTRY_TYPE_ADVERB, ENTRY_TYPE_ADJECTIVE, ENTRY_TYPE_VERB, \
    ENTRY_TYPE_PRONOUN, ENTRY_TYPE_PREPOSITION, ENTRY_TYPE_CONJUNCTION, ENTRY_TYPE_INTERJECTION, ENTRY_TYPE_IDIOM, \
    ENTRY_TYPE_PHRASAL_VERB, ENTRY_TYPE_PREFIX, ENTRY_TYPE_UNKNOWN, ENTRY_TYPE_SUFFIX
from lang.dictionary.types import EntryData, RecordingData, TranslationData, TranslationEntryData, ExampleData
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
    'suffiks': ENTRY_TYPE_SUFFIX,
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
        for entry_data in result['entries']:
            for meaning_data in entry_data['meanings']:
                entry_type = ENTRY_TYPES_MAP.get(meaning_data.get('part_of_speech'), ENTRY_TYPE_UNKNOWN)

                entry = entries_by_type.setdefault(
                    (entry_type, entry_data['text']), EntryData(
                        text=entry_data['text'],
                        language=entry_language,
                        type=entry_type,
                        source_url=entry_data['url'],
                        translations=[],
                        recordings=[RecordingData(audio_url=r['url']) for r in entry_data['recordings']]))

                translation = TranslationData(
                    language=translation_language,
                    type=entry_type,
                    entries=[TranslationEntryData(text=t['text'], source_url=t['url']) for t in meaning_data['translations']],
                    recordings=[RecordingData(audio_url=r['url']) for r in meaning_data['recordings']],
                    examples=[ExampleData(
                        text=e['text'], translation=e['translation'], recording=RecordingData(audio_url=e['recording']['url']))
                        for e in meaning_data['examples']])

                entry.translations.append(translation)

        return list(entries_by_type.values())
