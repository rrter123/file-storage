from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    # TODO: Make filenames unique since they all live on the same bucket (add id)
    file_object = models.FileField()
    organization = models.ForeignKey(
        "organization.Organization", on_delete=models.CASCADE, related_name="files"
    )

    @property
    def filename(self):
        return self.file_object.name.split("/")[-1]

    def __str__(self):
        return f"{self.filename}"


class Download(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="downloads")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="downloads")

    def __str__(self):
        return f"{self.file} - {self.user}"
