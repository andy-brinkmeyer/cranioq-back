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
        self.no_profile_user = User.objects.create_user('noprofile', email='noprofile@mail.com', password='test12345')

        gp_role = Role.objects.get(role='gp')
        spec_role = Role.objects.get(role='specialist')
        Profile.objects.create(user=self.gp, role=gp_role, title='Dr.', clinic_name='Test Clinic')
        Profile.objects.create(user=self.spec, role=spec_role, title='Dr.', clinic_name='Test Hospital')

        self.gp_token = Token.objects.get_or_create(user=self.gp)[0].key
        self.no_profile_user_token = Token.objects.get_or_create(user=self.no_profile_user)[0].key

    def tearDown(self) -> None:
        self.gp.delete()
        self.spec.delete()

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

    def test_put(self):
        # create userdata
        user_data = {
            'email': self.gp.email,
            'first_name': self.gp.first_name,
            'last_name': self.gp.last_name,
            'title': self.gp.profile.title,
            'clinic_name': self.gp.profile.clinic_name,
            'clinic_street': self.gp.profile.clinic_street,
            'clinic_city': self.gp.profile.clinic_city,
            'clinic_postcode': self.gp.profile.clinic_postcode
        }

        # try unauthenticated change
        self.client.credentials()
        response = self.client.put('/user/{}'.format(self.gp.id), user_data)
        self.assertEqual(response.status_code, 401, msg='User did not provied Token. 401 code was expected but instead '
                                                        'got {}'.format(response.status_code))

        # try to change data without haveing a profile
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.no_profile_user_token))
        response = self.client.put('/user/{}'.format(self.no_profile_user.id), user_data)
        self.assertEqual(response.status_code, 404, msg='View should return 404 since this user has no profile.')

        # provide incomplete data
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.gp_token))
        response = self.client.put('/user/{}'.format(self.gp.id))
        self.assertEqual(response.status_code, 400, msg='Incomplete data was provided. Expected 400 status code.')

        # try to change sombeody else's profile data
        response = self.client.put('/user/{}'.format(self.spec.id), user_data)
        self.assertEqual(response.status_code, 403, msg='Attempted to change data of another user. '
                                                        'Expected 403 status code.')

        # change own data
        user_data['clinic_name'] = 'Test Clinic 2'
        response = self.client.put('/user/{}'.format(self.gp.id), user_data)
        self.gp.refresh_from_db()
        self.assertEqual(response.status_code, 200, msg='Expected successfull 200 response.')
        self.assertEqual(self.gp.profile.clinic_name, user_data['clinic_name'], msg='Expected updated clinic name.')
