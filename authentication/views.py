from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            user_data = {
                'username': request.data['email'],
                'password': request.data['password']
            }
        except KeyError:
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        if user_data['username'] == '' or user_data['password'] == '':
            raise ValidationError({'error_message': 'One or more fields were left empty.'})
        serializer = self.serializer_class(data=user_data,
                                           context={'request': request})
        if not serializer.is_valid():
            raise ValidationError({'error_message': 'The email or password provided is incorrect.'})
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if hasattr(user, 'gp'):
            role = 'gp'
        elif hasattr(user, 'specialist'):
            role = 'specialist'
        else:
            role = 'anon'

        return Response({
            'token': token.key,
            'id': user.pk,
            'role': role
        })
