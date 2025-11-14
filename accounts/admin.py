from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'address', 'birth_date'),
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'address', 'birth_date'),
        }),
    )
