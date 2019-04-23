from django.urls import path, include, re_path

from lang.dictionary import views


urlpatterns = [
    re_path(r'entries/(?P<entry_id>[^/]+)/$', views.EntryView.as_view(), name='view-entry'),
    re_path(r'entries/$', views.EntriesView.as_view(), name='view-entries'),
]
