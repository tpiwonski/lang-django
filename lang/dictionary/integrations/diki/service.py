from lang.dictionary.db.entry import ENTRY_TYPE_NOUN, ENTRY_TYPE_ADVERB, ENTRY_TYPE_ADJECTIVE, ENTRY_TYPE_VERB, \
    ENTRY_TYPE_PRONOUN, ENTRY_TYPE_PREPOSITION, ENTRY_TYPE_CONJUNCTION, ENTRY_TYPE_INTERJECTION, ENTRY_TYPE_IDIOM, \
    ENTRY_TYPE_PHRASAL_VERB, ENTRY_TYPE_PREFIX, ENTRY_TYPE_UNKNOWN, ENTRY_TYPE_SUFFIX
from lang.dictionary.data import EntryData, RecordingData, TranslationData, TranslationEntryData, ExampleData, \
    HeadwordData
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

        entries_data = []
        for entry in result['entries']:
            entry_data = EntryData(
                language=entry_language,
                translations=[],
                headwords=[
                    HeadwordData(
                        text=h['text'],
                        source_url=h['url'],
                        recordings=[
                            RecordingData(audio_url=r['url'])
                            for r in h['recordings']])
                    for h in entry['headwords']])

            for meaning in entry['meanings']:
                part_of_speech = meaning.get('part_of_speech')
                if not part_of_speech:
                    entry_type = ENTRY_TYPE_UNKNOWN
                else:
                    entry_type = ENTRY_TYPES_MAP.get(part_of_speech)
                    assert entry_type is not None, "Unknown part of speech: {}".format(part_of_speech)

                translation_data = TranslationData(
                    language=translation_language,
                    type=entry_type,
                    entries=[
                        TranslationEntryData(
                            text=t['text'],
                            source_url=t['url'])
                        for t in meaning['translations']],
                    recordings=[
                        RecordingData(
                            audio_url=r['url'])
                        for r in meaning['recordings']],
                    examples=[
                        ExampleData(
                            text=e['text'],
                            translation=e['translation'],
                            recording=RecordingData(audio_url=e['recording']['url']))
                        for e in meaning['examples']])

                entry_data.translations.append(translation_data)

            entries_data.append(entry_data)

        return entries_data
