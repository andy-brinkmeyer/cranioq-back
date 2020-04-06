from rest_framework.serializers import ModelSerializer, CharField, PrimaryKeyRelatedField

from .models import Questionnaire, QuestionnaireTemplate, QuestionTemplate, Answer


class QuestionTemplateSerializer(ModelSerializer):
    type = CharField(source='type.type', read_only=True)
    category = CharField(source='category.name', read_only=True)

    class Meta:
        model = QuestionTemplate
        fields = ['id', 'type', 'category', 'question', 'description', 'answers']


class QuestionnaireTemplateSerializer(ModelSerializer):
    questions = QuestionTemplateSerializer(read_only=True, many=True)

    class Meta:
        model = QuestionnaireTemplate
        fields = ['id', 'name', 'description', 'questions']


class QuestionnairePostSerializer(ModelSerializer):
    template_id = PrimaryKeyRelatedField(queryset=QuestionnaireTemplate.objects.all())

    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'email', 'template_id', 'access_id']


class TemplateInformationSerializer(ModelSerializer):
    class Meta:
        model = QuestionnaireTemplate
        fields = ['id', 'name', 'version', 'description']


class AnswerSerializer(ModelSerializer):
    question_id = PrimaryKeyRelatedField(queryset=QuestionTemplate.objects.all())

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']


class QuestionnaireSerializer(ModelSerializer):
    template = QuestionnaireTemplateSerializer(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'access_id', 'email', 'completed', 'template', 'answers']
