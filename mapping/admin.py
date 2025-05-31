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
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('email',) #disable editing of the email field in admin change form


admin.site.register(CustomUser, CustomUserAdmin)