from rest_framework.serializers import ModelSerializer, CharField

from .models import Questionnaire, QuestionnaireTemplate, QuestionTemplate


class QuestionnaireSerializer(ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'email']


class QuestionTemplateSerializer(ModelSerializer):
    type = CharField(source='type.type', read_only=True)

    class Meta:
        model = QuestionTemplate
        fields = ['type', 'question', 'description', 'answers']


class QuestionnaireTemplateSerializer(ModelSerializer):
    questions = QuestionTemplateSerializer(read_only=True, many=True)

    class Meta:
        model = QuestionnaireTemplate
        fields = ['id', 'name', 'description', 'questions']
