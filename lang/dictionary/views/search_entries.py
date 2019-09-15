from django import forms

from lang.common.component import ComponentView
from lang.dictionary.controllers.search_entries import SearchEntries
from lang.dictionary.serializers import ViewEntryOutput


class SearchEntriesForm(forms.Form):
    q = forms.CharField(max_length=255, required=False)


class SearchEntriesView(ComponentView):
    fragment_id = 'search-entries'
    page_template = 'dictionary/pages/search_entries.html'
    fragment_template = 'dictionary/fragments/search_entries.html'
    search_entries_controller = SearchEntries()

    def get(self, request, *args, **kwargs):
        search_form = SearchEntriesForm(self.request.GET)
        context = {
            'search_form': search_form
        }
        if not search_form.is_valid():
            return self.render(context, **kwargs)

        text = search_form.cleaned_data['q']
        if text:
            entries = self.search_entries_controller.execute(text)
            context.update({
                'entries': [ViewEntryOutput(entry).data for entry in entries]
            })

        return self.render(context, **kwargs)
