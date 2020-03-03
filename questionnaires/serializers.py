from rest_framework.serializers import ModelSerializer

from .models import Questionnaire


class QuestionnaireSerializer(ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'email']
