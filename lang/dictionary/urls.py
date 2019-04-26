from django.urls import path, include, re_path

from lang.dictionary.views import current_date, entry_list, entry_view

urlpatterns = [
    re_path(r'entries/(?P<entry_id>[^/]+)/$', entry_view.EntryView.as_view(), name='entry-view'),
    re_path(r'entries/$', entry_list.EntryListView.as_view(), name='entry-list'),
    re_path(r'current-date/$', current_date.CurrentDateView.as_view(), name='current-date'),
]
