from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from .models import QuestionnaireTemplate

from .serializers import QuestionnaireSerializer, QuestionnaireTemplateSerializer


class QuestionnaireView(APIView):
    @staticmethod
    def post(request):
        request.data['template_id'] = 1
        questionnaire = QuestionnaireSerializer(data=request.data)
        try:
            agreed = request.data['agreed']
        except KeyError:
            agreed = False

        if not questionnaire.is_valid():
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not agreed:
            return Response({'error_message': 'Not agreed to terms and conditions.'},
                            status=status.HTTP_400_BAD_REQUEST)

        quest = questionnaire.create(questionnaire.data)
        return Response({'questionnaire_id': quest.id}, status=status.HTTP_201_CREATED)


class QuestionnaireTemplateView(APIView):
    @staticmethod
    def get(request, template_id):
        try:
            template = QuestionnaireTemplate.objects.get(pk=template_id)
        except ObjectDoesNotExist:
            return Response({'error_message': 'This template does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        template_serializer = QuestionnaireTemplateSerializer(template)
        return Response(template_serializer.data)
