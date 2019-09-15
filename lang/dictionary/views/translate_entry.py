import json

from django import forms

from lang.common.component import ComponentView
from lang.dictionary.controllers.add_entries import AddEntries
from lang.dictionary.controllers.translate_entry import TranslateEntry
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
                'payload': json.dumps(entries)
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
            if key.startswith('entry.'):
                _, entry_no, entry_prop = key.split('.')
                data.setdefault(entry_no, {})[entry_prop] = value
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
            if 'add' not in entry:
                continue

            translations = []
            for translation_no, translation in entry['translations'].items():
                translation_entries = []
                for translation_entry_no, translation_entry in translation['entries'].items():
                    translation_entry = translation_entry['entry']
                    if 'add' in translation_entry:
                        translation_entries.append(payload[int(entry_no)]['translations'][int(translation_no)]['entries'][int(translation_entry_no)])

                if translation_entries:
                    t = payload[int(entry_no)]['translations'][int(translation_no)]
                    t['entries'] = translation_entries
                    translations.append(t)

            if translations:
                entry = payload[int(entry_no)]
                entry['translations'] = translations
                entries.append(entry)

        entries = self.add_entries_controller.execute(entries)
        context = {
            'entries': [ViewEntryOutput(entry).data for entry in entries]
        }
        return self.render(context, **kwargs)
