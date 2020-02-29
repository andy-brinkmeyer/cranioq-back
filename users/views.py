from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

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
