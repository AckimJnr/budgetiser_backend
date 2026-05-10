from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('created_at', 'updated_at')}),
    )

admin.site.register(User, CustomUserAdmin)
