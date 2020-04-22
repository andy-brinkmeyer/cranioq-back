from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from users.models import Profile, Role
from users.serializers import UserSerializer


# Create your tests here.
class UserViewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        # create users
        self.gp = User.objects.create_user('gp', email='gp@mail.com', password='test12345')
        self.spec = User.objects.create_user('spec', email='spec@mail.com', password='test12345')

        gp_role = Role.objects.get(role='gp')
        spec_role = Role.objects.get(role='specialist')
        Profile.objects.create(user=self.gp, role=gp_role, title='Dr.', clinic_name='Test Clinic')
        Profile.objects.create(user=self.spec, role=spec_role, title='Dr.', clinic_name='Test Hospital')

        self.gp_token = Token.objects.get_or_create(user=self.gp)[0].key
        self.spec_token = Token.objects.get_or_create(user=self.spec)[0].key

    def test_get(self):
        # make non-authenticated request
        response = self.client.get('/user/{}'.format(self.gp.id))
        self.assertEqual(response.status_code, 401, msg='User did not provied Token. 401 code was expected but instead '
                                                        'got {}'.format(response.status_code))

        # make authenticated request with correct ID
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.gp_token))
        response = self.client.get('/user/{}'.format(self.gp.id))
        self.assertEqual(response.json(), UserSerializer(self.gp).data, msg='View returned wrong user data.'
                         .format(UserSerializer(self.gp).data))

        # use invalid user ID
        response = self.client.get('/user/100')
        self.assertEqual(response.status_code, 404, msg='View should return 404 since this user ID does not exist.')
