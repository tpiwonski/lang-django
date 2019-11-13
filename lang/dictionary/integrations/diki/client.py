from requests import Session
from bs4 import BeautifulSoup
import html
import re

# dict(
#     entities=list(
#         dict(
#             entry=str,
#             meanings=list(
#                 dict(
#                     part_of_peech=str,
#                     translations=list(
#                         dict(
#                             entry=str
#                         )
#                     )
#                 )
#             )
#         )
#     )
# )

DIKI_ROOT_URL = "https://diki.pl"
DIKI_DICTIONARY_SEGMENT = '/slownik-angielskiego?q='


class HtmlClient(object):
    
    def __init__(self):
        self.session = Session()

    def translate(self, entry):
        response = self.session.get("{}/{}".format(DIKI_ROOT_URL, entry))
        parser = HtmlParser()
        return parser.parse_results(response.content.decode('utf-8').replace('&apos;', "'").replace('&nbsp;', ' '))


class HtmlParser(object):
    DICTIONARY_EN_PL = 'angielsko-polski'
    DICTIONARY_PL_EN = 'polsko-angielski'
    ENTRY_NOT_FOUND = 'Nie znaleziono'
    REGEXP_TRANSLATION_USAGE_NOTES = re.compile(
        r'^(?P<translation>[^\(]+)'
        r'(?P<notes>\([^\(\)]+\)){0,1}'
        r'(?P<rest>.*){0,1}$', flags=re.IGNORECASE)

    def parse_results(self, content):
        content = BeautifulSoup(content, features="html.parser")

        first_paragraph_tag = content.select('#contentWrapper .dikiBackgroundBannerPlaceholder p')
        if first_paragraph_tag:
            first_paragraph = first_paragraph_tag[0].text.strip()
            if self.ENTRY_NOT_FOUND in first_paragraph:
                return None

        dictionary_tag = content.select('.dictionarySectionHeader .hide-below-xs')
        dictionary_name = dictionary_tag[0].text.strip()
        if self.DICTIONARY_EN_PL in dictionary_name:
            dictionary_name = ('en', 'pl')
        elif self.DICTIONARY_PL_EN in dictionary_name:
            dictionary_name = ('pl', 'en')
        else:
            raise NotImplementedError()

        left_column_tag = content.select('.diki-results-left-column')
        entries = []
        if left_column_tag:
            entries = self.parse_entries(left_column_tag[0])
        
        return dict(dictionary=dictionary_name, entries=entries)

    def parse_entries(self, content):
        entity_tags = content.find_all('div', class_='dictionaryEntity')
        entries = []
        for entity_tag in entity_tags:
            entries.append(self.parse_entry(entity_tag))

        return entries

    def parse_entry(self, content):
        entry_tags = content.select('.hws .hw')
        meanings = self.parse_meanings(content)

        headwords = []
        for entry_tag in entry_tags:
            text = entry_tag.text.strip()
            url_tag = entry_tag.find('a', class_='plainLink', recursive=False)
            if url_tag:
                url = '{}{}'.format(DIKI_ROOT_URL, url_tag['href'])
            else:
                url = '{}{}{}'.format(DIKI_ROOT_URL, DIKI_DICTIONARY_SEGMENT, text)

            recordings = []
            recordings_tag = entry_tag.find_next_sibling('span', class_='recordingsAndTranscriptions')
            if recordings_tag:
                recordings = self.parse_recordings(recordings_tag)

            headwords.append(dict(text=text, url=url, recordings=recordings))

        return dict(headwords=headwords, meanings=meanings)

    def parse_meanings(self, content):
        meanings = []
        
        entry_slices_tag = content.find('ol', class_='nativeToForeignEntrySlices', recursive=False)
        if entry_slices_tag:
            part_of_speech = self.parse_part_of_speech(entry_slices_tag)
            entry_slice_tags = entry_slices_tag.find_all('li', recursive=False)
            for entry_slice_tag in entry_slice_tags:
                meanings.append(self.parse_entry_slice(entry_slice_tag, part_of_speech))

        meanings_tags = content.find_all('ol', class_='foreignToNativeMeanings', recursive=False)
        for meanings_tag in meanings_tags:
            part_of_speech = self.parse_part_of_speech(meanings_tag)
            meaning_tags = meanings_tag.find_all('li', recursive=False)
            for meaning_tag in meaning_tags:
                meanings.append(self.parse_meaning(meaning_tag, part_of_speech))
        
        return meanings

    def parse_entry_slice(self, content, part_of_speech):
        translations = self.parse_translations(content)
        recordings = self.parse_recordings(content, css='.hw + .recordingsAndTranscriptions')
        examples = self.parse_examples(content)
        return dict(
            part_of_speech=part_of_speech, translations=translations, recordings=recordings, examples=examples)

    def parse_part_of_speech(self, content):
        part_of_speech_tag = content.find_previous_sibling('div', class_='partOfSpeechSectionHeader')
        if not part_of_speech_tag:
            return None

        part_of_speech = part_of_speech_tag.text.strip()
        return part_of_speech

    def parse_meaning(self, content, part_of_speech):
        translations = self.parse_translations(content)
        recordings = self.parse_recordings(content, css='.hw + .recordingsAndTranscriptions')
        examples = self.parse_examples(content)
        return dict(
            part_of_speech=part_of_speech, translations=translations, recordings=recordings, examples=examples)

    def parse_translations(self, content):
        translation_tags = content.find_all('span', class_='hw', recursive=False)
        translations = []
        for translation_tag in translation_tags:
            translation = self.parse_translation(translation_tag)
            if translation['notes']:
                for t in reversed(translations):
                    if not t['notes']:
                        t['notes'] = translation['notes']
                    else:
                        break

            translations.append(translation)

        return translations

    def parse_translation(self, content):
        url_tag = content.find('a', class_='plainLink')
        m = self.REGEXP_TRANSLATION_USAGE_NOTES.match(content.text.strip())

        text = m.group('translation').strip()
        notes = m.group('notes')
        notes = notes.strip("()").strip() if notes else ''

        return dict(text=text, url='{}{}'.format(DIKI_ROOT_URL, url_tag['href']), notes=notes)

    def parse_recordings(self, content, css=''):
        recording_tags = content.select('{} .hasRecording *[data-audio-url]'.format(css))
        recordings = []
        for recording_tag in recording_tags:
            recordings.append({
                'url': '{}{}'.format(DIKI_ROOT_URL, recording_tag['data-audio-url'])
            })

        return recordings

    def parse_examples(self, content):
        example_tags = content.select('.exampleSentence')
        examples = []
        for example_tag in example_tags:
            text = example_tag.next.strip()
            translation_tags = example_tag.select('.exampleSentenceTranslation')
            if not translation_tags:
                continue
    
            translation = translation_tags[0].text.strip().strip('()')
            recordings = self.parse_recordings(example_tag, css='.recordingsAndTranscriptions')
            if not recordings:
                continue

            examples.append({
                'text': html.unescape(text),
                'translation': html.unescape(translation),
                'recording': recordings[0]
            })

        return examples
