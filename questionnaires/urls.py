from django.urls import path

from . import views


urlpatterns = [
    path('quest', views.QuestionnaireView.as_view()),
    path('quest/<int:questionnaire_id>', views.QuestionnaireView.as_view()),
    path('quest/<str:access_id>', views.GuardianQuestionnaireView.as_view()),
    path('templates', views.QuestionnaireTemplatesView.as_view()),
    path('templates/<int:template_id>', views.QuestionnaireTemplateView.as_view())
]
