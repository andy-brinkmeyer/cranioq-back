import re
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """This route is used request the authtoken using user credentials."""

        # check if the required data was sent in ther equest body
        try:
            user_data = {
                'username': request.data['username'],
                'password': request.data['password']
            }
        except (KeyError, TypeError):
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_400_BAD_REQUEST)

        # check for empty fields
        if user_data['username'] == '' or user_data['password'] == '':
            raise ValidationError({'error_message': 'One or more fields were left empty.'})

        # use the serializer class provided by the rest_framework to virify the user, then fetch the user and token
        serializer = self.serializer_class(data=user_data,
                                           context={'request': request})
        if not serializer.is_valid():
            raise ValidationError({'error_message': 'The username or password provided is incorrect.'})
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # get the role of the user
        if hasattr(user, 'profile'):
            role = user.profile.role.role
        else:
            role = 'anon'

        return Response({
            'token': token.key,
            'id': user.pk,
            'role': role
        })


class VerifyView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """This route is used to verify an authtoken. It returns the id and role of the user on success."""

        user = request.user
        if user is AnonymousUser:
            return Response({'error_message': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if hasattr(user, 'profile'):
                role = user.profile.role.role
            else:
                role = 'anon'
        return Response({
            'id': user.pk,
            'role': role
        })


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        """This route is used to change the users password."""

        # check if the correct data is provided in the request body
        try:
            old_password = request.data['oldPassword']
            new_password = request.data['newPassword']
            repeated_password = request.data['repeatNewPassword']
        except (KeyError, TypeError):
            return Response({'error_message': 'Invalid data format.'}, status=status.HTTP_400_BAD_REQUEST)

        if type(old_password) != str or type(new_password) != str or type(repeated_password) != str:
            return Response({'error_message': 'The password must be strings'},
                            status=status.HTTP_400_BAD_REQUEST)

        # fetch the user and do some checks before changing the password or rejecting the request
        user = request.user
        if not user.check_password(old_password):
            return Response({'error_message': 'Wrong password.'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.check_password(new_password):
            return Response({'error_message': 'The new password must be different from the old one.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if new_password != repeated_password:
            return Response({'error_message': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if not re.search('[0-9]+', new_password):
            return Response({'error_message': 'The password must contain at least one number.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'error_message': 'The password must be at least 8 characters long.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)
