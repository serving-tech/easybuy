from django.contrib import admin
from .models import Customer, Property, Partners, Testimonials


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'location', 'created_at','is_featured')
    search_fields = ('title', 'location',)
    list_filter = ('status', 'propertytyp','is_featured')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')
    search_fields = ('name', 'email', 'subject')

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'details', 'facebook', 'instagram', 'linkedin', 'twitter')
    search_fields = ('name', 'details')
    list_filter = ('details',)

@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'created_at')
    search_fields = ('name', 'position')

