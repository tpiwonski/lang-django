from django import forms

from lang.dictionary.controllers import SearchEntries
from lang.dictionary.views.base import PageView
from lang.dictionary.views.current_date import CurrentDateView


class SearchEntriesForm(forms.Form):
    q = forms.CharField(max_length=255)


class SearchEntriesView(PageView):
    fragment_id = 'search-entries'
    page_template = 'dictionary/pages/search_entries.html'
    fragment_template = 'dictionary/fragments/search_entries.html'
    component_classes = [CurrentDateView]
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
                'entries': entries
            })

        return self.render(context, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     search_form = SearchEntriesForm(request.POST)
    #     context = {
    #         'search_form': search_form
    #     }
    #     if not search_form.is_valid():
    #         return self.render_fragment(context, **kwargs)

    #     entries = self.search_entries_controller.execute(text=search_form.cleaned_data['q'])
    #     context.update({
    #         'entries': entries
    #     })
    #     # return self.render_fragment(context, **kwargs)

    #     return self.render_response(context, [CurrentDateView, SearchEntriesView], **kwargs)

        # return self.render_response(context, {
        #     'current-date': 'dictionary/fragments/current_date.html',
        #     'search-entries': self.fragment_template
        # }, **kwargs)

        # context.update(self.get_context_data(**kwargs))
        # content = {
        #     'current-date': render_to_string('dictionary/fragments/current_date.html', context, request),
        #     'search-entries': render_to_string(self.fragment_template, context, request)
        # }
        
        # return HttpResponse(json.dumps(content), content_type="application/json")
