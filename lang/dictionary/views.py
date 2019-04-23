from django.shortcuts import render
from django.views.generic import TemplateView

from lang.dictionary.controllers import GetAllEntries, GetEntry


class EntriesView(TemplateView):
    template_name = 'dictionary/pages/entries.html'
    get_all_entries_controller = GetAllEntries()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = self.get_all_entries_controller.execute()
        context['entries'] = entries
        return context


class EntryView(TemplateView):
    template_name = 'dictionary/pages/entry.html'
    get_entry_controller = GetEntry()

    def get_context_data(self, entry_id, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.get_entry_controller.execute(entry_id)
        context['entry'] = entry
        return context
