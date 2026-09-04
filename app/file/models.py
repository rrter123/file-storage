from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    file_object = models.FileField()
    organization = models.ForeignKey(
        "organization.Organization", on_delete=models.CASCADE
    )


class Download(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
