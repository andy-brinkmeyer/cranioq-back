from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DataError

from .serializers import UserSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, user_id):
        try:
            user = get_user_model().objects.get(pk=int(user_id))
        except ObjectDoesNotExist:
            return Response({'error_message': 'This user does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    @staticmethod
    def put(request, user_id):
        if request.user.id != user_id:
            return Response({'error_message': 'No permissions to change this data.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = get_user_model().objects.get(pk=int(user_id))
        except ObjectDoesNotExist:
            return Response({'error_message': 'This user does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if not hasattr(user, 'profile'):
            return Response({'error_message': 'This user does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            email = request.data['email']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            title = request.data['title']
            clinic_name = request.data['clinic_name']
            clinic_street = request.data['clinic_street']
            clinic_city = request.data['clinic_city']
            clinic_postcode = request.data['clinic_postcode']
        except (KeyError, TypeError):
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_400_BAD_REQUEST)

        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.profile.title = title
        user.profile.clinic_name = clinic_name
        user.profile.clinic_street = clinic_street
        user.profile.clinic_city = clinic_city
        user.profile.clinic_postcode = clinic_postcode

        try:
            user.save()
            user.profile.save()
        except DataError:
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'displayable_message': 'Details changed.'
        }
        return Response(response)
