import json
from dataclasses import asdict

from django import forms

from lang.common.component import ComponentView
from lang.dictionary.controllers.add_entries import AddEntries
from lang.dictionary.controllers.translate_entry import TranslateEntry
from lang.dictionary.data import EntryData, RecordingData, TranslationEntryData, TranslationData, ExampleData, \
    HeadwordData
from lang.dictionary.serializers import ViewEntryOutput


class TranslateEntryForm(forms.Form):
    q = forms.CharField(max_length=255, required=False)


class TranslateEntryView(ComponentView):
    fragment_id = 'translate-entry'
    page_template = 'dictionary/pages/translate_entry.html'
    fragment_template = 'dictionary/fragments/translate_entry.html'
    translate_entry_controller = TranslateEntry()

    def get(self, request, *args, **kwargs):
        translate_form = TranslateEntryForm(request.GET)
        context = {
            'translate_form': translate_form
        }
        if not translate_form.is_valid():
            return self.render(context, **kwargs)

        text = translate_form.cleaned_data['q']
        if text:
            entries = self.translate_entry_controller.execute(text)
            context.update({
                'entries': entries,
                'payload': json.dumps([asdict(e) for e in entries])
            })

        return self.render(context, **kwargs)


class AddEntryTranslationsView(ComponentView):
    fragment_id = 'translate-entry'
    fragment_template = 'dictionary/fragments/entry_list.html'
    add_entries_controller = AddEntries()
    
    def post(self, request, *args, **kwargs):
        payload = json.loads(request.POST.get('payload'))
        data = {}
        for key, value in request.POST.items():
            if key.startswith('headword.'):
                _, entry_no, headword_no, headword_prop = key.split('.')
                data.setdefault(entry_no, {}).setdefault('headwords', {}).setdefault(headword_no, {})[headword_prop] = value
            elif key.startswith('translation.'):
                _, entry_no, translation_no, translation_entry_no, translation_prop = key.split('.')
                data.setdefault(entry_no, {}).setdefault('translations', {}).setdefault(translation_no, {}).setdefault(
                    'entries', {}).setdefault(translation_entry_no, {}).setdefault('entry', {})[
                    translation_prop] = value
            elif key.startswith('example.'):
                _, entry_no, translation_no, example_no, example_prop = key.split('.')
                data.setdefault(entry_no, {}).setdefault('translations', {}).setdefault(translation_no, {}).setdefault(
                    'examples', {}).setdefault(example_no, {})[example_prop] = value

        entries = []
        for entry_no, entry in data.items():
            if not any([h.get('add') for h in entry['headwords'].values()]):
                continue

            translations = []
            for translation_no, translation in entry['translations'].items():
                translation_entries = []
                for translation_entry_no, translation_entry in translation['entries'].items():
                    translation_entry = translation_entry['entry']
                    if 'add' in translation_entry:
                        translation_entry_data = payload[int(entry_no)]['translations'][int(translation_no)]['entries'][int(translation_entry_no)]
                        translation_entry = TranslationEntryData(
                            text=translation_entry_data['text'], source_url=translation_entry_data['source_url'])
                        translation_entries.append(translation_entry)

                if translation_entries:
                    translation_data = payload[int(entry_no)]['translations'][int(translation_no)]
                    translation = TranslationData(
                        language=translation_data['language'],
                        type=translation_data['type'],
                        entries=translation_entries,
                        recordings=[RecordingData(audio_url=r['audio_url']) for r in translation_data['recordings']],
                        examples=[ExampleData(
                            text=e['text'], translation=e['translation'],
                            recording=RecordingData(audio_url=e['recording']['audio_url']))
                                for e in translation_data['examples']])

                    translations.append(translation)

            if translations:
                entry_data = payload[int(entry_no)]
                entryxxx = EntryData(
                    language=entry_data['language'],
                    headwords=[HeadwordData(
                        text=entry_data['headwords'][int(h_no)]['text'],
                        source_url=entry_data['headwords'][int(h_no)]['source_url'],
                        recordings=[RecordingData(audio_url=r['audio_url']) for r in entry_data['headwords'][int(h_no)]['recordings']]
                    ) for h_no, h in entry['headwords'].items() if h['add']],
                    translations=translations)

                entries.append(entryxxx)

        entries = self.add_entries_controller.execute(entries)
        context = {
            'entries': [ViewEntryOutput(entry).data for entry in entries]
        }
        return self.render(context, **kwargs)
