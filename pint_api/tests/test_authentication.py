from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

class AuthenticationTests(APITestCase):
    def setUp(self):
      # Create the user who will authenticate:
      self.user_username = 'myuser'
      self.user_password = 'mypassword'

      self.user = User.objects.create_user(
          username=self.user_username,
          email='myuser@example.com',
          password=self.user_password
      )

    def test_obtain_refresh_token(self):
        """
        Ensure we can obtain and refresh a JWT when providing valid credentials.
        """
        data = { 'username': self.user_username, 'password': self.user_password}
        response_obtain = self.client.post('/api/token/', data, format='json')

        self.assertEqual(response_obtain.status_code, status.HTTP_200_OK)
        access_token = response_obtain.data['access']
        assert bool(access_token)

        # Refresh the access token:
        refresh_token = response_obtain.data['refresh']
        response_refresh = self.client.post('/api/token/refresh/', {'refresh': refresh_token}, format='json')

        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        refreshed_access_token = response_refresh.data['access']
        assert bool(refreshed_access_token)