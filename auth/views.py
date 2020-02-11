from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, ParseError

from .serializers import UserSerializer
from .response_generators import gen_login_response


class LoginView(APIView):
    @staticmethod
    def post(request):
        try:
            credentials = JSONParser().parse(request)
            username = credentials['email']
            password = credentials['password']
        except (ParseError, KeyError):
            username = ''
            password = ''
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_data = UserSerializer(user)
            success = True
        else:
            user_data = UserSerializer()
            success = False
        return Response(gen_login_response(success, user_data))
