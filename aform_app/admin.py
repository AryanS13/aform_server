from django.contrib import admin
from .models import Form, FieldProperty, Field
# Register your models here.

admin.site.register(Form)
admin.site.register(FieldProperty)
admin.site.register(Field)