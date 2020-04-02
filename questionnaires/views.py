import random
import string

from cranioq_back.global_variables import FRONT_END_ADDRESS

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from .models import QuestionnaireTemplate, Answer, Questionnaire
from .email import ADDRESSES

from .serializers import QuestionnairePostSerializer, QuestionnaireTemplateSerializer, TemplateInformationSerializer, \
    QuestionnaireSerializer


class QuestionnaireView(APIView):
    @staticmethod
    def get(request, **kwargs):
        if 'questionnaire_id' not in kwargs:
            return Response({'error_message': 'No questionnaire ID provided.'}, status.HTTP_400_BAD_REQUEST)

        try:
            questionnaire = Questionnaire.objects.get(pk=kwargs['questionnaire_id'])
        except ObjectDoesNotExist:
            return Response({'error_message': 'The questionnaire does not exist.'}, status.HTTP_404_NOT_FOUND)
        questionnaire_serializer = QuestionnaireSerializer(questionnaire)
        return Response(questionnaire_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, **kwargs):
        questionnaire_data = request.data

        # generate random access id
        access_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        while len(Questionnaire.objects.filter(access_id=access_id)) > 0:
            access_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        questionnaire_data['access_id'] = access_id

        questionnaire = QuestionnairePostSerializer(data=questionnaire_data)
        try:
            agreed = request.data['agreed']
        except KeyError:
            agreed = False

        if not questionnaire.is_valid():
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not agreed:
            return Response({'error_message': 'Not agreed to terms and conditions.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # send email
        mail_text = 'Dear Guardian, \n\n Please fill out the following questionnaire about your child: ' \
                    '{}{} \n\n Best regards,\n Your CranioQ Team'.format(FRONT_END_ADDRESS, access_id)
        send_mail('CranioQ Questionnaire Available', mail_text, ADDRESSES['info'], [questionnaire_data['email']])

        quest = questionnaire.create(questionnaire.data)
        return Response({'questionnaire_id': quest.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request, **kwargs):
        try:
            questionnaire_id = request.data['questionnaireID']
            answers = request.data['answers']
        except KeyError:
            return Response({'error_message': 'Invalid data format.'}, status.HTTP_400_BAD_REQUEST)

        if questionnaire_id < 0:
            return Response({'error_message': 'Invalid Questionnaire ID, ID must be greater than 0.'},
                            status.HTTP_400_BAD_REQUEST)

        if type(answers) != dict:
            return Response('Invalid data format.', status.HTTP_400_BAD_REQUEST)

        for key in answers:
            current_answer = Answer.objects.filter(questionnaire=questionnaire_id, question=key)
            if len(current_answer) != 0:
                current_answer.delete()
            answer = Answer(questionnaire_id=questionnaire_id, question_id=key, answer=answers[key])
            answer.save()
        return Response(status=status.HTTP_200_OK)


class QuestionnaireTemplatesView(APIView):
    @staticmethod
    def get(request):
        templates = QuestionnaireTemplate.objects.all()
        serialized_templates = TemplateInformationSerializer(templates, many=True)
        return Response(serialized_templates.data, status=status.HTTP_200_OK)


class QuestionnaireTemplateView(APIView):
    @staticmethod
    def get(request, template_id):
        try:
            template = QuestionnaireTemplate.objects.get(pk=template_id)
        except ObjectDoesNotExist:
            return Response({'error_message': 'This template does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        template_serializer = QuestionnaireTemplateSerializer(template)
        return Response(template_serializer.data)


class EmailTest(APIView):
    @staticmethod
    def get(request):
        send_mail('Test Subject', 'This is the message.', ADDRESSES['info'], ['ucabrin@ucl.ac.uk'])
        return Response('Done')
