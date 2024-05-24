from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization

class UserAdmin(UserAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Organization)

