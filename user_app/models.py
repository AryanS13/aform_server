from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=False)



