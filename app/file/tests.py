from account.models import Employee
from django.contrib.auth.models import User
from django.test import TestCase
from organization.models import Organization
from rest_framework.test import APIClient

from file.models import Download, File


class FileViewsetTestCase(TestCase):
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
        self.file = File.objects.create(organization=self.organization)
        Download.objects.create(file=self.file, user=self.user)
        Download.objects.create(file=self.file, user=self.user)
        file_2 = File.objects.create(organization=self.organization)
        Download.objects.create(file=file_2, user=self.user)

    def test_list(self):
        res = self.client.get("/files")
        self.assertEqual(res.status_code, 200)
        org = next(f for f in res.json() if f["id"] == self.file.id)
        self.assertEqual(org["organization"], self.organization.id)
        self.assertEqual(org["download_count"], 2)


class FileViewsetQueryTestCase(TestCase):
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
            res = self.client.get("/files")
        self.assertEqual(res.status_code, 200)


class DownloadByViewsetsTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="1")
        self.user, _ = User.objects.get_or_create(
            username="test", email="test@test.com"
        )
        self.user.set_password("test")
        self.user.save()
        Employee.objects.create(user=self.user, organization=self.organization)

        user_2 = User.objects.create(username="test2")
        Employee.objects.create(user=user_2, organization=self.organization)

        self.file = File.objects.create(organization=self.organization)
        file_2 = File.objects.create(organization=self.organization)

        self.download = Download.objects.create(file=self.file, user=self.user)
        self.download_2 = Download.objects.create(file=self.file, user=self.user)
        self.download_3 = Download.objects.create(file=self.file, user=user_2)
        self.download_file_2 = Download.objects.create(file=file_2, user=self.user)

        self.client = APIClient()
        self.client.login(username="test", password="test")

    def test_downloads_by_user(self):
        res = self.client.get(f"/downloadsByUser/{self.user.id}")
        self.assertEqual(res.status_code, 200)

        downloads_data = res.json()
        self.assertEqual(len(downloads_data), 3)
        expected_ids = [self.download.id, self.download_2.id, self.download_file_2.id]
        self.assertListEqual([d["id"] for d in downloads_data], expected_ids)

        download = next(d for d in downloads_data if d["id"] == self.download.id)

        self.assertEqual(download["file"], self.file.id)
        self.assertEqual(
            download["download_time"],
            self.download.download_time.isoformat().replace("+00:00", "Z"),
        )

    def test_downloads_by_file(self):
        res = self.client.get(f"/downloadsByFile/{self.file.id}")
        self.assertEqual(res.status_code, 200)

        downloads_data = res.json()
        self.assertEqual(len(downloads_data), 3)
        expected_ids = [self.download.id, self.download_2.id, self.download_3.id]
        self.assertListEqual([d["id"] for d in downloads_data], expected_ids)

        download = next(d for d in downloads_data if d["id"] == self.download.id)
        self.assertEqual(download["user"], self.user.id)
        self.assertEqual(
            download["download_time"],
            self.download.download_time.isoformat().replace("+00:00", "Z"),
        )
