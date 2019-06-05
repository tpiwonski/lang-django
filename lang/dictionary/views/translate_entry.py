from django import forms
from django.shortcuts import redirect

from lang.dictionary.controllers import TranslateEntry, AddEntries
from lang.dictionary.views.base import PageView
from lang.dictionary.views.current_date import CurrentDateView


class TranslateEntryForm(forms.Form):
    q = forms.CharField(max_length=255)


class TranslateEntryView(PageView):
    fragment_id = 'translate-entry'
    page_template = 'dictionary/pages/translate_entry.html'
    fragment_template = 'dictionary/fragments/translate_entry.html'
    component_classes = [CurrentDateView]
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
                'entries': entries
            })

        return self.render(context, **kwargs)


class AddEntryTranslationsView(PageView):
    fragment_id = 'translate-entry'
    fragment_template = 'dictionary/fragments/entry_list.html'
    component_classes = [CurrentDateView]
    add_entries_controller = AddEntries()
    
    def post(self, request, *args, **kwargs):
        data = {}
        for key, value in request.POST.items():
            if key.startswith('entry.'):
                _, entry_no, entry_prop = key.split('.')
                data.setdefault(entry_no, {})[entry_prop] = value
            elif key.startswith('translation.'):
                _, entry_no, translation_no, translation_entry_no, translation_prop = key.split('.')
                data.setdefault(entry_no, {}).setdefault('translations', {}).setdefault(translation_no, {}).setdefault('entries', {}).setdefault(translation_entry_no, {}).setdefault('entry', {})[translation_prop] = value
            elif key.startswith('example.'):
                _, entry_no, translation_no, example_no, example_prop = key.split('.')
                data.setdefault(entry_no, {}).setdefault('translations', {}).setdefault(translation_no, {}).setdefault('examples', {}).setdefault(example_no, {})[example_prop] = value

        entries = []
        for entry in data.values():
            if 'add' in entry:
                translations = []
                for translation in entry['translations'].values():
                    for translation_entry in translation['entries'].values():
                        translation_entry = translation_entry['entry']
                        if 'add' in translation_entry:
                            translations.append({
                                'text': translation_entry['text'],
                                'language': translation_entry['language'],
                                'examples': [example for example in translation.get('examples', {}).values()]
                            })

                if translations:
                    entries.append({
                        'text': entry['text'],
                        'language': entry['language'],
                        'translations': translations
                    })

        entries = self.add_entries_controller.execute(entries)
        context = {
            'entries': entries
        }
        return self.render(context, **kwargs)
