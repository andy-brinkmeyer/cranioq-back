from django.contrib import admin

from .models import Questionnaire, QuestionnaireTemplate, QuestionTemplate


# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(QuestionnaireTemplate)
admin.site.register(QuestionTemplate)
