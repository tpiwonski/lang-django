from django.urls import path, re_path

from lang.dictionary.api import views

urlpatterns = [
    re_path(r'entries/(?P<guid>[^/]+)/$', views.EntryView.as_view(), name='api-entry'),
    re_path(r'entries/$', views.EntriesView.as_view(), name='api-entries'),
    re_path(r'translations/$', views.TranslationsView.as_view(), name='api-translations'),
    re_path(r'search/(?P<text>[^/]+)$', views.SearchEntryView.as_view(), name='api-search'),
]
