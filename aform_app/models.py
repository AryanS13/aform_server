from django.db import models
from user_app.models import Organization

# Create your models here.

class Form(models.Model):
    title = models.CharField(max_length=300, blank=False, null=False)
    organization = models.ForeignKey(Organization, blank=False, null=True, related_name='organization', on_delete=models.CASCADE)
