from requests import Session
from bs4 import BeautifulSoup

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

class HtmlClient(object):
    
    def __init__(self):
        self.session = Session()

    def translate(self, entry):
        response = self.session.get("https://diki.pl/{}".format(entry))
        parser = HtmlParser()
        return parser.parse_results(response.content)


class HtmlParser(object):
    
    def __init__(self):
        pass

    def parse_results(self, content):
        content = BeautifulSoup(content)
        left_column_tag = content.select('.diki-results-left-column')
        entries = []
        if left_column_tag:
            entries = self.parse_entries(left_column_tag[0])
        
        return dict(entries=entries)

    def parse_entries(self, content):
        entity_tags = content.find_all('div', class_='dictionaryEntity')
        entries = []
        for entity_tag in entity_tags:
            entries.append(self.parse_entry(entity_tag))

        return entries

    def parse_entry(self, content):
        entry_tag = content.select('.hws .hw') #find('div', clss_='hws').find('span', class_='hw')
        text = entry_tag[0].text.strip()
        meanings = self.parse_meanings(content)
        return dict(text=text, meanings=meanings)
    
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
        return dict(part_of_speech=part_of_speech, translations=translations)

    def parse_part_of_speech(self, content):
        part_of_speech_tag = content.find_previous_sibling('div', class_='partOfSpeechSectionHeader')
        part_of_speech = part_of_speech_tag.text.strip()
        return part_of_speech

    def parse_meaning(self, content, part_of_speech):
        translations = self.parse_translations(content)
        return dict(part_of_speech=part_of_speech, translations=translations)

    def parse_translations(self, content):
        translation_tags = content.find_all('span', class_='hw', recursive=False)
        translations = []
        for translation_tag in translation_tags:
            translations.append(self.parse_translation(translation_tag))
        
        return translations

    def parse_translation(self, content):
        return dict(text=content.text.strip())
