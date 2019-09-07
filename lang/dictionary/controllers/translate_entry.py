from lang.dictionary.integrations.diki.service import TranslationService
from lang.dictionary.models import Entry


class TranslateEntry(object):
    entry_repository = Entry.objects
    translation_service = TranslationService()

    def execute(self, text):
        results = self.translation_service.translate(text)
        return results
