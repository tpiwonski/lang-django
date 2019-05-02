from .client import HtmlClient


class TranslationService(object):

    def __init__(self):
        self.client = HtmlClient()

    def translate(self, text: str):
        result = self.client.translate(text)
        entries = []
        for entry in result['entries']:
            translations = []
            for meaning in entry['meanings']:
                for translation in meaning['translations']:
                    translations.append({
                        'text': translation['text'],
                        'language': 'pl'
                    })
            
            entries.append({
                'text': entry['text'],
                'language': 'en',
                'translations': translations
            })

        return entries
