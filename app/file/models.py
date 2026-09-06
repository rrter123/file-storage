from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


def file_unique_name(instance, filename):
    # Add datetime to the filename to ensure uniqueness
    filename_list = filename.split(".")
    filename_list.insert(-1, datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    return ".".join(filename_list)


class File(models.Model):
    file_object = models.FileField(upload_to=file_unique_name)
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
    download_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file} - {self.user}"
