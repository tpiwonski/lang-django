import uuid

from rest_framework.serializers import Serializer, CharField, ChoiceField, UUIDField, ModelSerializer, SerializerMethodField

from dictionary.models import Entry, LANGUAGES, Translation


class EntryInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class TranslatedEntryOutput(ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'text', 'language']


class EntryOutput(ModelSerializer):
    translations = TranslatedEntryOutput(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'text', 'language', 'translations']


class TranslationInput(Serializer):
    text = CharField()
    language = ChoiceField(choices=LANGUAGES)


class AddTranslationInput(Serializer):
    entry = EntryInput()
    translations = TranslationInput(many=True)


class AddTranslationOutput(ModelSerializer):
    
    class Meta:
        model = Entry
        fields = ['id']


class AddEntry(object):
    entry_repository = Entry.objects

    def execute(self, text, language):
        entry = Entry.create(text=text, language=language)
        self.entry_repository.save(entry)
        return EntryOutput(entry).data


class GetAllEntries(object):
    entry_repository = Entry.objects

    def execute(self):
        entries = self.entry_repository.get_all()
        return [EntryOutput(entry).data for entry in entries]


class FindEntry(object):
    entry_repository = Entry.objects

    def execute(self, text):
        entries = self.entry_repository.find_word(text)
        return [EntryOutput(entry).data for entry in entries]


class AddTranslation(object):
    entry_repository = Entry.objects

    def execute(self, entry, translations):
        source_entry = self.entry_repository.find_word(entry['text'], entry['language'])
        if source_entry:
            source_entry = source_entry[0]
        else:
            source_entry = Entry.create(entry['text'], entry['language'])

        for translation in translations:
            translated_entry = self.entry_repository.find_word(translation['text'], translation['language'])
            if translated_entry:
                translated_entry = translated_entry[0]
            else:
                translated_entry = Entry.create(translation['text'], translation['language'])

            if not source_entry.has_translation(translated_entry):
                source_entry.add_translation(translated_entry)

        self.entry_repository.save(source_entry)
        return AddTranslationOutput(source_entry).data
