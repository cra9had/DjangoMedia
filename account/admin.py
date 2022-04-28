from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from .models import User


ChosenMediaContent = apps.get_model('content', 'ChosenMediaContent')


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    def get_chooses(self, obj):
        print(dir(obj))
        return obj.email

    fieldsets = (
        (None, {'fields': ('email', 'password', 'activation_key',)}),
        (_('Personal info'), {'fields': ('fullname',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'fullname'),
        }),
    )
    list_display = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
