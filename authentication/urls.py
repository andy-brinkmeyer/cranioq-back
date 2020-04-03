from django.urls import path

from . import views


urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('verify', views.VerifyView.as_view())
]
