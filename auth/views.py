from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        user_data = {
            'username': request.data['email'],
            'password': request.data['password']
        }
        if user_data['username'] == '' or user_data['password'] == '':
            raise ValidationError({'errorMessage': 'One or more fields were left empty.'})
        serializer = self.serializer_class(data=user_data,
                                           context={'request': request})
        if not serializer.is_valid():
            raise ValidationError({'errorMessage': 'The email or password provided is incorrect.'})
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name
        })
