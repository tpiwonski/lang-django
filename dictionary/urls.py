from django.urls import path, re_path

from dictionary.api.word import WordView, WordsView, AddTranslationView


urlpatterns = [
    re_path(r'word/(?P<word>[^/]+)/$', WordView.as_view(), name='word'),
    re_path(r'word/$', WordsView.as_view(), name='words'),
    re_path(r'translation/$', AddTranslationView.as_view(), name='translation')
]
