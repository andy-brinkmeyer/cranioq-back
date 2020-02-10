from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login

from .response_models import construct_login_response


def login_user(request):
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        response = construct_login_response(True)
    else:
        response = construct_login_response(False)
    return JsonResponse(response)


def register(request):
    return HttpResponse('register')
