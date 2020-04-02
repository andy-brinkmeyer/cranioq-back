from django.db import models
from django.contrib.postgres import fields


# questionnaire model
class Answer(models.Model):
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    question = models.ForeignKey('QuestionTemplate', on_delete=models.PROTECT)
    answer = fields.ArrayField(base_field=models.CharField(max_length=200), size=10, blank=True)

    def __str__(self):
        return 'Answer: {}'.format(self.answer)


class Questionnaire(models.Model):
    patient_id = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    template = models.ForeignKey('QuestionnaireTemplate', on_delete=models.PROTECT)
    completed = models.BooleanField(default=False)
    access_id = models.CharField(max_length=8)

    def __str__(self):
        return 'Questionnaire for: {}'.format(self.patient_id)

    class Meta:
        indexes = [models.Index(fields=('patient_id',))]


# models for questionnaire templating
class QuestionnaireTemplate(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=20)
    description = models.TextField()
    questions = models.ManyToManyField('QuestionTemplate')

    def __str__(self):
        return 'Questionnaire: {} v{}'.format(self.name, self.version)


class QuestionCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name


class QuestionType(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.type


class QuestionTemplate(models.Model):
    type = models.ForeignKey('QuestionType', on_delete=models.PROTECT)
    question = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    answers = fields.ArrayField(base_field=models.CharField(max_length=200), size=10, blank=True)
    category = models.ForeignKey('QuestionCategory', on_delete=models.PROTECT)

    def __str__(self):
        return 'Question: {}'.format(self.question)
