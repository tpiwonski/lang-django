from django.urls import path, re_path

from dictionary.api import views

urlpatterns = [
    re_path(r'word/(?P<word>[^/]+)/$', views.WordAPIView.as_view(), name='word'),
    re_path(r'word/$', views.WordsAPIView.as_view(), name='words'),
    re_path(r'translation/$', views.TranslationAPIView.as_view(), name='translation')
]
