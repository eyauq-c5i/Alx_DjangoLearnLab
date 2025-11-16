from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'date_of_birth', 'profile_photo')}),
    )
    
    search_fields = ('email', 'username')

admin.site.register(CustomUser, CustomUserAdmin)
