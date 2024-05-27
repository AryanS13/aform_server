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

class Form(models.Model):
    title = models.CharField(max_length=300, blank=False, null=False)
    organization = models.ForeignKey(Organization, blank=False, null=True, related_name='organization', on_delete=models.CASCADE)

class Field(models.Model):
    title = models.CharField(max_length=500, blank=False, null=False)
    description = models.CharField(max_length=1000, blank=False, null=False)
    ref = models.CharField(max_length=200, blank=False, null=False)
    type = models.CharField(choices=QUESTION_TYPES, default=QUESTION_TYPES[1], null=False, blank=False)
    
    layout = models.JSONField(blank=True, null=True)

    properties = models.OneToOneField(FieldProperty, on_delete=models.CASCADE, primary_key=True)

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields', null=True, blank=True)
    order = models.IntegerField(default=0)

class Logic(models.Model):
    FIELD = 'field'
    HIDDEN = 'constant'

    TYPE_CHOICES = {
        Field: 'field',
        HIDDEN: 'hidden'
    }

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='logic', blank=True, null=True)
    type = models.CharField(choices=TYPE_CHOICES, default=FIELD, null=False, blank=False)
    ref = models.CharField(max_length=200, blank=False, null=False)
    order = models.IntegerField(default=0)

class Condition(models.Model):
    CONDITION_OPERATORS = [
        ('equal', 'equal'),
        ('is', 'is'),
        ('is_not', 'is_not'),
        ('greater', 'greater'),
        ('less_than', 'less_than'),
        ('and', 'and'),
        ('or', 'or')
    ]

    operator = models.CharField(max_length=10, choices=CONDITION_OPERATORS, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=1)

class ConditionVariable(models.Model):
    condition = models.ForeignKey(Condition, related_name='vars', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=200)


class Actions(models.Model):
    JUMP = 'jump'
    ADD = 'add'
    SUBTRACT = 'subtract'
    MULTIPLY = 'multiply'
    DIVIDE = 'divide'

    ACTION_CHOICES = {
        JUMP: 'jump',
        ADD: 'add',
        SUBTRACT: 'subtract',
        MULTIPLY: 'multiply',
        DIVIDE: 'divide'
    }
    logic=models.ForeignKey(Logic, related_name='actions', blank=True, null=True, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    action = models.CharField(choices=ACTION_CHOICES, null=False, blank=False)
    condition = models.OneToOneField(Condition, null=True, blank=True, related_name='condition', on_delete=models.CASCADE)

    details = models.JSONField()

