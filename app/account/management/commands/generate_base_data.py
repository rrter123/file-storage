from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from organization.models import Organization

from account.models import Employee


class Command(BaseCommand):
    help = "Generates base data for testing the app"

    def handle(self, *args, **kwargs):
        organization_1, _ = Organization.objects.get_or_create(
            name="Organization 1 Apples"
        )
        organization_2, _ = Organization.objects.get_or_create(
            name="Organization 2 Carrots"
        )
        root_user, created = User.objects.get_or_create(
            username="root", email="root@test.com", is_staff=True, is_superuser=True
        )
        if created:
            root_user.set_password("root")
            root_user.save()
            Employee.objects.create(user=root_user, organization=organization_1)
        user, created = User.objects.get_or_create(
            username="test", email="test@test.com"
        )
        if created:
            user.set_password("test")
            user.save()
            Employee.objects.create(user=user, organization=organization_2)
        print("Successfully created objects")
