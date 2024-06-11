from django.contrib import admin
from .models import Form, FieldProperty, Field, Actions, Condition
# Register your models here.

admin.site.register(Form)
admin.site.register(FieldProperty)
admin.site.register(Field)
admin.site.register(Actions)
admin.site.register(Condition)