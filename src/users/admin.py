from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Доп. информация', {'fields': ('pol', 'vozrast', 'ves', 'rost')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Доп. информация', {'fields': ('pol', 'vozrast', 'ves', 'rost')}),
    )
