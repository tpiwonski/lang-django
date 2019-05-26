from .client import HtmlClient


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
                for translation in meaning['translations']:
                    translations.append({
                        'text': translation['text'],
                        'language': translation_language,
                        'recordings': meaning['recordings'],
                        'examples': meaning['examples']
                    })
            
            entries.append({
                'text': entry['text'],
                'language': entry_language,
                'translations': translations,
                'recordings': entry['recordings']
            })

        return entries
