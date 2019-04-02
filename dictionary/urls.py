from django.urls import path, re_path

from dictionary.api.entry import EntriesView, TranslationsView


urlpatterns = [
    # re_path(r'word/(?P<word>[^/]+)/$', WordView.as_view(), name='word'),
    re_path(r'entries/$', EntriesView.as_view(), name='dictionary:entries'),
    re_path(r'translations/$', TranslationsView.as_view(), name='dictionary:translations')
]
