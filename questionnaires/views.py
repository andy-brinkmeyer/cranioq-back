import random
import string

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import QuestionnaireTemplate, Answer, Questionnaire

from .serializers import QuestionnairePostSerializer, QuestionnaireTemplateSerializer, TemplateInformationSerializer, \
    QuestionnaireSerializer, QuestionnaireListSerializer, QuestionTemplateSerializer, AnswerSerializer, \
    NotificationsSerializer


class QuestionnaireListView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            page = int(request.query_params['page'])
        except (KeyError, ValueError):
            page = 1
        try:
            page_size = int(request.query_params['pageSize'])
            if page_size > 1000:
                page_size = 100
            elif page_size < 1:
                page_size = 1
        except (KeyError, ValueError):
            page_size = 100
        start = (page - 1) * page_size
        end = page * page_size

        # create query parameters
        query_params = dict()
        if 'patientID' in request.query_params:
            query_params['patient_id__contains'] = str(request.query_params['patientID'])

        if 'completedGP' in request.query_params:
            if request.query_params['completedGP'] == 'true':
                query_params['completed_gp'] = True
            elif request.query_params['completedGP'] == 'false':
                query_params['completed_gp'] = False

        if 'completedGuardian' in request.query_params:
            if request.query_params['completedGuardian'] == 'true':
                query_params['completed_guardian'] = True
            elif request.query_params['completedGuardian'] == 'false':
                query_params['completed_guardian'] = False

        if 'reviewed' in request.query_params:
            if request.query_params['reviewed'] == 'true':
                query_params['reviewed_by__isnull'] = False
            elif request.query_params['reviewed'] == 'false':
                query_params['reviewed_by__isnull'] = True

        if 'reviewedBy' in request.query_params:
            if 'reviewed_by__isnull' in query_params:
                del query_params['reviewed_by__isnull']
            query_params['reviewed_by__last_name__contains'] = str(request.query_params['reviewedBy'])

        try:
            role = request.user.profile.role.role
        except AttributeError:
            return Response({'error_message': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)

        if role == 'gp':
            questionnaires = Questionnaire.objects.filter(gp=request.user, **query_params)\
            .order_by('-created')[start:end]
        elif role == 'specialist':
            questionnaires = Questionnaire.objects.filter(**query_params).order_by('-created')[start:end]
        else:
            return Response({'error_message': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = QuestionnaireListSerializer(questionnaires, many=True)
        return Response(serializer.data)


class QuestionnaireView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, **kwargs):
        if 'questionnaire_id' not in kwargs:
            return Response({'error_message': 'No questionnaire ID provided.'}, status.HTTP_400_BAD_REQUEST)

        try:
            questionnaire = Questionnaire.objects.get(pk=kwargs['questionnaire_id'])
        except ObjectDoesNotExist:
            return Response({'error_message': 'The questionnaire does not exist.'}, status.HTTP_404_NOT_FOUND)

        try:
            role = request.user.profile.role.role
        except AttributeError:
            return Response({'error_message': 'Not authorized. You either need to be a GP or Specialist.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if role == 'specialist':
            questions = questionnaire.template.questions.all()
            answers = questionnaire.answers.all()
        elif role == 'gp':
            questions = questionnaire.template.questions.filter(role__role='gp').order_by('id')
            answers = questionnaire.answers.filter(question__in=questions)
        else:
            return Response({'error_message': 'Not authorized. You either need to be a GP or Specialist.'},
                            status=status.HTTP_403_FORBIDDEN)

        template_data = QuestionnaireTemplateSerializer(questionnaire.template).data
        template_data['questions'] = QuestionTemplateSerializer(questions, many=True).data

        answer_data = AnswerSerializer(answers, many=True).data

        questionnaire_data = QuestionnaireSerializer(questionnaire).data
        questionnaire_data['template'] = template_data
        questionnaire_data['answers'] = answer_data
        return Response(questionnaire_data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, **kwargs):
        questionnaire_data = request.data

        # check if user is GP
        try:
            if request.user.profile.role.role != 'gp':
                return Response({'error_message': 'Only GPs can create new questionnaires.'},
                                status=status.HTTP_403_FORBIDDEN)
        except AttributeError:
            return Response({'error_message': 'Only GPs can create new questionnaires.'},
                            status=status.HTTP_403_FORBIDDEN)
        questionnaire_data['gp_id'] = request.user.id

        # generate random access id
        access_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
        while len(Questionnaire.objects.filter(access_id=access_id)) > 0:
            access_id = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
        questionnaire_data['access_id'] = access_id

        questionnaire = QuestionnairePostSerializer(data=questionnaire_data)
        try:
            agreed = request.data['agreed']
        except (KeyError, TypeError):
            agreed = False

        if not questionnaire.is_valid():
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not agreed:
            return Response({'error_message': 'Not agreed to terms and conditions.'},
                            status=status.HTTP_400_BAD_REQUEST)

        quest = questionnaire.create(questionnaire.data)
        return Response({'questionnaire_id': quest.id, 'access_id': access_id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request, **kwargs):
        try:
            questionnaire_id = request.data['questionnaireID']
            answers = request.data['answers']
            completed = request.data['completed']
        except (KeyError, TypeError):
            return Response({'error_message': 'Invalid data format.'}, status.HTTP_400_BAD_REQUEST)

        if questionnaire_id < 0:
            return Response({'error_message': 'Invalid Questionnaire ID, ID must be greater than 0.'},
                            status.HTTP_400_BAD_REQUEST)

        try:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        except ObjectDoesNotExist:
            return Response({'error_message': 'This questionaire does not exist or is no longer valid.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if questionnaire.completed_gp:
            return Response({'error_message': 'This questionnaire has already been submitted. No changes allowed.'},
                            status=status.HTTP_403_FORBIDDEN)

        if type(answers) != dict:
            return Response('Invalid data format.', status.HTTP_400_BAD_REQUEST)

        # get the users role
        try:
            role = request.user.profile.role.role
        except AttributeError:
            return Response({'error_message': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        # get all the allowed questions
        question_set = questionnaire.template.questions.all()
        allowed_questions = {}
        for question in question_set:
            allowed_questions[question.id] = question

        for question_id in answers:
            question_id = int(question_id)
            if question_id not in allowed_questions:
                return Response({'error_message': 'The answer with questionID {} is not part of this questionaire'
                                .format(question_id)}, status=status.HTTP_400_BAD_REQUEST)
            if allowed_questions[question_id].role.role != role:
                return Response({'error_message': 'You do not have the permission to change some of the questions'},
                                status=status.HTTP_401_UNAUTHORIZED)
            current_answer = Answer.objects.filter(questionnaire=questionnaire,
                                                   question=allowed_questions[question_id]).first()
            if current_answer is None:
                answer = Answer(questionnaire=questionnaire, question=allowed_questions[question_id],
                                answer=answers[str(question_id)])
                answer.save()
            else:
                current_answer.answer = answers[str(question_id)]
                current_answer.save()

        questionnaire.completed_gp = completed
        questionnaire.save()

        return Response(status=status.HTTP_200_OK)


class GuardianQuestionnaireView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, access_id):
        if type(request.user) is not AnonymousUser:
            return Response({'error_message': 'This route is for non-authenticated users only.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            questionnaire = Questionnaire.objects.get(access_id=access_id)
        except ObjectDoesNotExist:
            return Response({'error_message': 'The questionnaire does not exist.'}, status.HTTP_404_NOT_FOUND)

        if questionnaire.completed_guardian:
            return Response({'error_message': 'The questionnaire does not exist.'}, status.HTTP_404_NOT_FOUND)

        questions = questionnaire.template.questions.filter(role__role='anon').order_by('id')
        answers = questionnaire.answers.filter(question__in=questions)

        template_data = QuestionnaireTemplateSerializer(questionnaire.template).data
        template_data['questions'] = QuestionTemplateSerializer(questions, many=True).data

        answer_data = AnswerSerializer(answers, many=True).data

        questionnaire_data = QuestionnaireSerializer(questionnaire).data
        questionnaire_data['template'] = template_data
        questionnaire_data['answers'] = answer_data
        return Response(questionnaire_data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request, access_id):
        try:
            questionnaire = Questionnaire.objects.get(access_id=access_id)
        except ObjectDoesNotExist:
            return Response({'error_message': 'This questionaire does not exist or is no longer valid.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if questionnaire.completed_guardian:
            return Response({'error_message': 'This questionnaire has already been submitted. No changes allowed.'},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            answers = request.data['answers']
            completed = request.data['completed']
        except (KeyError, TypeError):
            return Response({'error_message': 'Invalid data format.'}, status.HTTP_400_BAD_REQUEST)

        if type(answers) != dict:
            return Response('Invalid data format.', status.HTTP_400_BAD_REQUEST)

        # check if the user is anon
        if type(request.user) is not AnonymousUser:
            return Response({'error_message': 'This route is for non-authenticated users only.'},
                            status=status.HTTP_403_FORBIDDEN)

        # get all the allowed questions
        question_set = questionnaire.template.questions.all()
        allowed_questions = {}
        for question in question_set:
            allowed_questions[question.id] = question

        for question_id in answers:
            question_id = int(question_id)
            if question_id not in allowed_questions:
                return Response({'error_message': 'The answer with questionID {} is not part of this questionaire'
                                .format(question_id)}, status=status.HTTP_400_BAD_REQUEST)
            if allowed_questions[question_id].role.role != 'anon':
                return Response({'error_message': 'You do not have the permission to change some of the questions'},
                                status=status.HTTP_403_FORBIDDEN)
            current_answer = Answer.objects.filter(questionnaire=questionnaire,
                                                   question=allowed_questions[question_id]).first()
            if current_answer is None:
                answer = Answer(questionnaire=questionnaire, question=allowed_questions[question_id],
                                answer=answers[str(question_id)])
                answer.save()
            else:
                current_answer.answer = answers[str(question_id)]
                current_answer.save()

            questionnaire.completed_guardian = completed
            questionnaire.save()

        return Response(status=status.HTTP_200_OK)


class QuestionnaireTemplatesView(APIView):
    permission_classes = [IsAuthenticated]

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


class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, questionnaire_id):
        try:
            role = request.user.profile.role.role
        except AttributeError:
            return Response({'error_message': 'No permissions to perfrom this request.'},
                            status=status.HTTP_403_FORBIDDEN)

        if role != 'specialist':
            return Response({'error_message': 'No permissions to perfrom this request.'},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            review = request.data['review']
        except (KeyError, TypeError):
            return Response({'error_message': 'Invalid data format.'}, status=status.HTTP_400_BAD_REQUEST)

        if type(review) is not list:
            return Response({'error_message': 'Invalid data format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        except ObjectDoesNotExist:
            return Response({'error_message': 'The questionnaire does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        questionnaire.review = review
        questionnaire.reviewed_by = request.user
        questionnaire.dismiss_notification = False
        questionnaire.save()

        return Response(status=status.HTTP_200_OK)


class NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):

        try:
            role = request.user.profile.role.role
        except AttributeError:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if role == 'gp':
            questionnaires = Questionnaire.objects.\
                filter(gp=request.user, completed_gp=True, completed_guardian=True, dismiss_notification=False).\
                exclude(review__len=0).order_by('-created')
        elif role == 'specialist':
            questionnaires = Questionnaire.objects.filter(completed_gp=True, completed_guardian=True, review__len=0)\
                .order_by('-created')
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = NotificationsSerializer(questionnaires, many=True)
        return Response(serializer.data)
    
    @staticmethod
    def put(request, questionnaire_id):
        try:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        try:
            dismiss = request.data['dismiss']
        except (KeyError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        questionnaire.dismiss_notification = dismiss
        questionnaire.save()
            
        return Response(status=status.HTTP_200_OK)

