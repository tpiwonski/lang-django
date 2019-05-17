from django import forms

from lang.common.component import ComponentView
from lang.dictionary.controllers import TranslateEntry
from lang.dictionary.models import Entry
from lang.dictionary.views.base import PageView
from lang.dictionary.views.current_date import CurrentDateView


class TranslateForm(forms.Form):
    text = forms.CharField(max_length=255)


class TranslateEntryView(PageView):
    fragment_id = 'translate-entry'
    page_template = 'dictionary/pages/translate_entry.html'
    fragment_template = 'dictionary/fragments/translate_entry.html'
    component_classes = [CurrentDateView]
    translate_entry_controller = TranslateEntry()

    def get(self, request, *args, **kwargs):
        context = {
            'translate_form': TranslateForm()
        }
        return self.render(context, **kwargs)

    def post(self, request, *args, **kwargs):
        translate_form = TranslateForm(request.POST)
        context = {
            'translate_form': translate_form
        }
        if not translate_form.is_valid():
            return self.render(context, **kwargs)
        
        entries = self.translate_entry_controller.execute(**translate_form.cleaned_data)
        context.update({
            'entries': entries
        })
        return self.render(context, **kwargs)


class DeleteEntriesForm(forms.Form):

    def __init__(self, entries, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        for entry in entries:
            self.fields['entry_{}'.format(entry['id'])] = forms.BooleanField()
            for translation in entry['translations']:
                self.fields['translation_{}'.format(translation['id'])] = forms.BooleanField()


class DeleteEntriesView(ComponentView):
    fragment_template = 'dictionary/fragments/entry_deleted.html'
    entry_repository = Entry.objects

    def post(self, request, *args, **kwargs):
        for name, value in request.POST.items():
            if name.startswith('entry_'):
                self.entry_repository.delete_entry_with_translations(value)
            elif name.startswith('translation_'):
                self.entry_repository.delete_entry(value)

        return self.render_fragment({}, **kwargs)
