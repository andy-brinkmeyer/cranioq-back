from django.db import models
from django.contrib.postgres import fields


# questionnaire model
class Questionnaire(models.Model):
    patient_id = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    template = models.ForeignKey('QuestionnaireTemplate', on_delete=models.PROTECT)

    def __str__(self):
        return 'Questionnaire for: {}'.format(self.patient_id)

    class Meta:
        indexes = [models.Index(fields=('patient_id',))]


# models for questionnaire templating
class QuestionnaireTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return 'Questionnaire: {}'.format(self.title)


class QuestionTemplate(models.Model):
    type = models.ForeignKey('QuestionType', on_delete=models.PROTECT, )
    question = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    answers = fields.ArrayField(base_field=models.CharField(max_length=200), size=10, blank=True)
    templates = models.ManyToManyField('QuestionnaireTemplate')

    def __str__(self):
        return 'Question: {}'.format(self.question)


class QuestionType(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.type
