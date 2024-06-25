from django.contrib.auth.models import AbstractUser
from django.db import models

class App(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    app = models.ForeignKey(App, on_delete=models.CASCADE, null=True, blank=True)
    field_extra = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
