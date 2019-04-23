from django.shortcuts import render
from django.views.generic import TemplateView

from lang.dictionary.controllers import GetAllEntries


class EntriesView(TemplateView):
    template_name = 'dictionary/pages/entries.html'
    get_all_entries_controller = GetAllEntries()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entries = self.get_all_entries_controller.execute()
        context['entries'] = entries
        return context
