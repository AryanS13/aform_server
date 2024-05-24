from django.db import models
from user_app.models import Organization
from .utils import QUESTION_TYPES

# Create your models here.properties

class FieldProperty(models.Model):
    STAR = 1
    RATING_CHOICES = {
        STAR: 'star'
    }

    allow_multiple_selection = models.BooleanField(default=False)
    randomize = models.BooleanField(default=False)
    allow_other_choice = models.CharField(max_length=100, blank=True, null=True)
    vertical_alignment = models.BooleanField(default=True)
    supersized = models.BooleanField(default=False)
    show_labels = models.BooleanField(default=True)
    alphabetical_order = models.BooleanField(default=False)
    hide_marks = models.BooleanField(default=True)
    button_text = models.CharField(default='Continue')
    steps = models.IntegerField(default = 10)
    shape = models.CharField(choices=RATING_CHOICES, default=STAR)
    start_at_one = models.BooleanField(default=False)


    choices = models.JSONField(blank=True, null=True)
    lables = models.JSONField(blank=True, null=True)

class Field(models.Model):
    title = models.CharField(max_length=500, blank=False, null=False)
    description = models.CharField(max_length=1000, blank=False, null=False)
    ref = models.CharField(max_length=200, blank=False, null=False, unique=True)
    type = models.CharField(choices=QUESTION_TYPES, default=QUESTION_TYPES[1], null=False, blank=False)
    
    layout = models.JSONField(blank=True, null=True)

    properties = models.OneToOneField(FieldProperty, on_delete=models.CASCADE, primary_key=True)

class Form(models.Model):
    title = models.CharField(max_length=300, blank=False, null=False)
    organization = models.ForeignKey(Organization, blank=False, null=True, related_name='organization', on_delete=models.CASCADE)
    fields = models.ManyToManyField(Field)
