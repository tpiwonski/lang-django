from django.urls import path, include


urlpatterns = [
    path('dictionary/', include('lang.dictionary.urls'))
]
