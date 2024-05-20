# django packages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# local packages
from pycun_pruebas_unitarias.apps.users.models import User


# Register your models here.
admin.site.register(User, UserAdmin)
