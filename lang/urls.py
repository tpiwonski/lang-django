from django.urls import path, include


urlpatterns = [
    path('dictionary/', include('lang.dictionary.urls')),
    path('api/dictionary/', include('lang.dictionary.api.urls')),
]
