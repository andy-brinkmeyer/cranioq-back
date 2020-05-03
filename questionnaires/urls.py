from django.urls import path

from . import views


urlpatterns = [
    path('', views.QuestionnaireListView.as_view()),
    path('quest', views.QuestionnaireView.as_view()),
    path('quest/<int:questionnaire_id>', views.QuestionnaireView.as_view()),
    path('quest/<int:questionnaire_id>/review', views.ReviewView.as_view()),
    path('quest/<str:access_id>', views.GuardianQuestionnaireView.as_view()),
    path('templates', views.QuestionnaireTemplateListView.as_view()),
    path('templates/<int:template_id>', views.QuestionnaireTemplateView.as_view()),
    path('notify', views.NotificationsView.as_view()),
    path('notify/<int:questionnaire_id>', views.NotificationsView.as_view()),
]
