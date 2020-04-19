from rest_framework.serializers import ModelSerializer, CharField, PrimaryKeyRelatedField, SlugRelatedField

from django.contrib.auth import get_user_model
from .models import Questionnaire, QuestionnaireTemplate, QuestionTemplate, Answer


class QuestionTemplateSerializer(ModelSerializer):
    type = CharField(source='type.type', read_only=True)
    category = CharField(source='category.name', read_only=True)
    role = SlugRelatedField(read_only=True, slug_field='role')

    class Meta:
        model = QuestionTemplate
        fields = ['id', 'type', 'category', 'role', 'question', 'description', 'answers']


class QuestionnaireTemplateSerializer(ModelSerializer):
    class Meta:
        model = QuestionnaireTemplate
        fields = ['id', 'name', 'description']


class QuestionnairePostSerializer(ModelSerializer):
    template_id = PrimaryKeyRelatedField(queryset=QuestionnaireTemplate.objects.all())
    gp_id = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'email', 'template_id', 'access_id', 'gp_id']


class TemplateInformationSerializer(ModelSerializer):
    class Meta:
        model = QuestionnaireTemplate
        fields = ['id', 'name', 'version', 'description']


class AnswerSerializer(ModelSerializer):
    question_id = PrimaryKeyRelatedField(queryset=QuestionTemplate.objects.all())

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name']


class QuestionnaireSerializer(ModelSerializer):
    reviewed_by = UserInfoSerializer()

    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'gp_id', 'access_id', 'email', 'completed_gp', 'completed_guardian',
                  'created', 'review', 'reviewed_by']


class QuestionnaireListSerializer(ModelSerializer):
    gp = UserInfoSerializer()

    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'gp', 'access_id', 'email', 'completed_gp', 'completed_guardian',
                  'created', 'review']
        
class NotificationsSerializer(ModelSerializer):

    class Meta:
        model = Questionnaire
        fields = ['id']
