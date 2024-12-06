from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import NewUser, Profile

# Inline class for Profile to display it on NewUser admin page
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Custom UserAdmin to handle the NewUser model
class CustomUserAdmin(BaseUserAdmin):
    model = NewUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Fields for email and password
        ('Personal info', {'fields': ('first_name', 'last_name')}),  # Personal info fields
        ('Permissions', {'fields': ('is_staff', 'is_active')}),  # Permissions fields
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = [ProfileInline]  # Display Profile inline when editing a NewUser

# Register the custom user admin
admin.site.register(NewUser, CustomUserAdmin)
