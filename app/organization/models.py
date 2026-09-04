from django.db import models


class Organization(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name
