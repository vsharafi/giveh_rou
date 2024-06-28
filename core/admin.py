from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin 


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', ]


    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": ('email',),
            },
        ),
    )
