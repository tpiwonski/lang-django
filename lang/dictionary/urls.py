from django.urls import path, include, re_path

from lang.dictionary.views import entry_list, view_entry, add_entry, edit_entry, translate_entry, search_entries, delete_entry

urlpatterns = [
    re_path(r'entries/(?P<entry_id>[^/]+)/$', view_entry.ViewEntry.as_view(), name='entry-view'),
    # re_path(r'entries/(?P<entry_id>[^/]+)/edit$', entry_view.EntryView.as_view(), name='entry-view'),
    re_path(r'all-entries/$', entry_list.ViewAllEntries.as_view(), name='all-entries'),
    re_path(r'search-entries/$', search_entries.SearchEntriesView.as_view(), name='search-entries'),
    re_path(r'add-entry/$', add_entry.AddEntryView.as_view(), name='add-entry'),
    re_path(r'edit-entry/(?P<entry_id>[^/]+)/$', edit_entry.EditEntryView.as_view(), name='edit-entry'),
    re_path(r'delete-entry/(?P<entry_id>[^/]+)/$', delete_entry.DeleteEntryView.as_view(), name='delete-entry'),
    re_path(r'translate-entry/$', translate_entry.TranslateEntryView.as_view(), name='translate-entry'),
    re_path(r'add-entries/$', translate_entry.AddEntryTranslationsView.as_view(), name='add-entries'),
    # re_path(r'delete-entries/$', translate_entry.DeleteEntriesView.as_view(), name='delete-entries'),
    # re_path(r'current-date/$', current_date.CurrentDateView.as_view(), name='current-date'),
    re_path(r'$', search_entries.SearchEntriesView.as_view(), name='search-entries'),
]
