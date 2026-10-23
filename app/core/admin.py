"""
Django admin customization.
"""


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# gettext_lazy used to place titles in each user info section
# in /change page
# rename to BaseUserAdmin to avoid conflicts with django UserAdmin
from core import models

# Register your models here.


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_filter = ("email", "name")
    list_display = ["email", "name", "is_staff", "is_active", "is_superuser"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    # classes: ('wide', ) is a CSS from djgango (find in documentation)
    # this is to enable the /add page > add_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(models.User, UserAdmin)
# we need to specify ,UserAdmin) so that it picks the page
# display class we defined, otherwise it uses the default
