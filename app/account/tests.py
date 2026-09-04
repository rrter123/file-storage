from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class UserViewSetAccessTestCase(TestCase):
    URL = "/users"

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username="test", email="test@test.com"
        )
        self.user.set_password("test")
        self.user.save()
        self.client = APIClient()
        self.client.login(username="test", password="test")

    def test_regular_user_can_not_access(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 403)

    def test_staff_user_can_access(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200)
