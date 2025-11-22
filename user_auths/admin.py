from django.contrib import admin
from user_auths.models import CustomUser
from .forms import CustomUserRegistrationForm
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserRegistrationForm

admin.site.register(CustomUser, CustomUserAdmin)    