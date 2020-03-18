from django.contrib import admin

from .models import Questionnaire, QuestionnaireTemplate, QuestionTemplate, QuestionCategory, Answer


# Register your models here.
admin.site.register(Questionnaire)
admin.site.register(QuestionnaireTemplate)
admin.site.register(QuestionTemplate)
admin.site.register(QuestionCategory)
admin.site.register(Answer)
