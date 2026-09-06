from account.models import Employee
from django.contrib.auth.models import User
from django.test import TestCase
from file.models import Download, File
from rest_framework.test import APIClient

from organization.models import Organization


class OrganizationViewsetTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="1")
        self.user, _ = User.objects.get_or_create(
            username="test", email="test@test.com"
        )
        self.user.set_password("test")
        self.user.save()
        Employee.objects.create(user=self.user, organization=self.organization)
        self.client = APIClient()
        self.client.login(username="test", password="test")
        file = File.objects.create(organization=self.organization)
        Download.objects.create(file=file, user=self.user)
        Download.objects.create(file=file, user=self.user)
        organization_2 = Organization.objects.create(name="2")
        file_2 = File.objects.create(organization=organization_2)
        Download.objects.create(file=file_2, user=self.user)
        Download.objects.create(file=file_2, user=self.user)

    def test_list(self):
        res = self.client.get("/organizations")
        self.assertEqual(res.status_code, 200)
        org = next(o for o in res.json() if o["id"] == self.organization.id)
        self.assertEqual(org["name"], self.organization.name)
        self.assertEqual(org["download_count"], 2)


class OrganizationViewsetQueryTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="1")
        self.user, _ = User.objects.get_or_create(
            username="test", email="test@test.com"
        )
        self.user.set_password("test")
        self.user.save()
        Employee.objects.create(user=self.user, organization=self.organization)
        self.client = APIClient()
        self.client.login(username="test", password="test")

    def create_data(self, i):
        user = User.objects.create(username=f"test_{i}")
        org = Organization.objects.create(name="Test")
        Employee.objects.create(organization=org, user=user)
        file = File.objects.create(organization=self.organization)
        file_2 = File.objects.create(organization=org)
        Download.objects.create(file=file, user=user)
        Download.objects.create(file=file, user=self.user)
        Download.objects.create(file=file_2, user=user)

    def test_n_plus_1(self):
        for i in range(3):
            self.create_data(i)
        with self.assertNumQueries(3):
            res = self.client.get("/organizations")
        self.assertEqual(res.status_code, 200)
