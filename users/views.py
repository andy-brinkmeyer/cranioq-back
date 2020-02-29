from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DataError

from .serializers import UserSerializer


class UserView(APIView):
    @staticmethod
    def get(request, user_id):
        try:
            user = User.objects.get(pk=int(user_id))
        except ObjectDoesNotExist:
            return Response({'error_message': 'This user does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    @staticmethod
    def put(request, user_id):
        try:
            user = User.objects.get(pk=int(user_id))
        except ObjectDoesNotExist:
            return Response({'error_message': 'This user does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            email = request.data['email']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
        except KeyError:
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        try:
            user.save()
        except DataError:
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        response = {
            'update_success': True,
            'displayable_message': 'Details changed.'
        }
        return Response(response)
