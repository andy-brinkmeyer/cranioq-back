from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('user/', include('users.urls')),
    path('quests/', include('questionnaires.urls')),
    path('admin/', admin.site.urls)
]
