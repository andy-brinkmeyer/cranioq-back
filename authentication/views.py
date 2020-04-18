from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import AllowAny


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            user_data = {
                'username': request.data['username'],
                'password': request.data['password']
            }
        except (KeyError, TypeError):
            return Response({'error_message': 'Wrong data format.'}, status=status.HTTP_400_BAD_REQUEST)

        if user_data['username'] == '' or user_data['password'] == '':
            raise ValidationError({'error_message': 'One or more fields were left empty.'})
        serializer = self.serializer_class(data=user_data,
                                           context={'request': request})
        if not serializer.is_valid():
            raise ValidationError({'error_message': 'The username or password provided is incorrect.'})
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

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
