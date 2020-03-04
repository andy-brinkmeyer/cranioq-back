from django.db import models


# questionnaire model
class Questionnaire(models.Model):
    patient_id = models.CharField(max_length=100)
    email = models.CharField(max_length=200)

    class Meta:
        indexes = [models.Index(fields=('patient_id',))]
