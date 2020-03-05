from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from .serializers import QuestionnaireSerializer


class QuestionnaireView(APIView):
    @staticmethod
    def post(request):
        questionnaire = QuestionnaireSerializer(data=request.data)
        try:
            agreed = request.data['agreed']
        except KeyError:
            agreed = False

        if not questionnaire.is_valid():
            return Response({'error_message': 'Wrong data format.'}, status=HTTP_400_BAD_REQUEST)
        elif not agreed:
            return Response({'error_message': 'Not agreed to terms and conditions.'}, status=HTTP_400_BAD_REQUEST)

        quest = questionnaire.create(questionnaire.data)
        return Response({'questionnaire_id': quest.id}, status=HTTP_201_CREATED)
