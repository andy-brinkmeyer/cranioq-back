from rest_framework.serializers import ModelSerializer, CharField, PrimaryKeyRelatedField, SlugRelatedField

from django.contrib.auth import get_user_model
from .models import Questionnaire, QuestionnaireTemplate, QuestionTemplate, Answer


class QuestionTemplateSerializer(ModelSerializer):
    """This class is used for serializing question templates. It does not support write operations."""

    type = CharField(source='type.type', read_only=True)
    category = CharField(source='category.name', read_only=True)
    role = SlugRelatedField(read_only=True, slug_field='role')

    class Meta:
        model = QuestionTemplate
        fields = ['id', 'type', 'category', 'role', 'question', 'description', 'answers']


class QuestionnaireTemplateSerializer(ModelSerializer):
    """This class is used for serializing basic questionnaire template information. It does not return questions."""

    class Meta:
        model = QuestionnaireTemplate
        fields = ['id', 'name', 'description']


class QuestionnairePostSerializer(ModelSerializer):
    """This class provides an interface for writing questionnaire data."""

    template_id = PrimaryKeyRelatedField(queryset=QuestionnaireTemplate.objects.all())
    gp_id = PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'email', 'template_id', 'access_id', 'gp_id']


class TemplateInformationSerializer(ModelSerializer):
    """This class is used for serializing basic template information."""

    class Meta:
        model = QuestionnaireTemplate
        fields = ['id', 'name', 'version', 'description']


class AnswerSerializer(ModelSerializer):
    """This class serializes answers."""

    question_id = PrimaryKeyRelatedField(queryset=QuestionTemplate.objects.all())

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']


class UserInfoSerializer(ModelSerializer):
    """This class serializes some user information that is usually needed together with the questionnaire data."""

    title = CharField(source='profile.title', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'title']


class QuestionnaireSerializer(ModelSerializer):
    """This class serializes a questionnaire."""

    reviewed_by = UserInfoSerializer()

    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'gp_id', 'access_id', 'email', 'completed_gp', 'completed_guardian',
                  'created', 'review', 'reviewed_by']


class QuestionnaireListSerializer(ModelSerializer):
    """This class is used to serialize the questionnaire data in a format used for a list view."""
    gp = UserInfoSerializer()
    reviewed_by = UserInfoSerializer()

    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id', 'gp', 'access_id', 'email', 'completed_gp', 'completed_guardian',
                  'created', 'review', 'reviewed_by']


class NotificationsSerializer(ModelSerializer):
    """This serializers is used to serialize notifications."""
    class Meta:
        model = Questionnaire
        fields = ['id', 'patient_id']
