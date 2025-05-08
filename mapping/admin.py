from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        # "username",
        "is_staff",
        "is_active",
    ]
    list_filter = ("is_staff", "is_active", "is_superuser")


admin.site.register(CustomUser, CustomUserAdmin)