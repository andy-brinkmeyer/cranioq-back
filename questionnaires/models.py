from django.db import models
from django.contrib.postgres import fields


# questionnaire model
class Questionnaire(models.Model):
    patient_id = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)

    class Meta:
        indexes = [models.Index(fields=('patient_id',))]


# models for questionnaire templating
class QuestionnaireTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()


class QuestionTemplate(models.Model):
    type = models.CharField(max_length=30)
    question = models.CharField(max_length=500)
    text = models.TextField()
    answers = fields.ArrayField(base_field=models.CharField(max_length=200), size=10)
