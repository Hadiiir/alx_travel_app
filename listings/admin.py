"""
Admin configuration for the listings app.
"""
from django.contrib import admin
from .models import Listing, Review


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """
    Admin interface for Listing model.
    """
    list_display = [
        'title', 'property_type', 'location', 'price_per_night',
        'max_guests', 'host', 'is_active', 'created_at'
    ]
    list_filter = ['property_type', 'is_active', 'created_at', 'max_guests']
    search_fields = ['title', 'location', 'description', 'host__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'property_type')
        }),
        ('Location & Pricing', {
            'fields': ('location', 'latitude', 'longitude', 'price_per_night')
        }),
        ('Property Details', {
            'fields': ('max_guests', 'bedrooms', 'bathrooms', 'amenities')
        }),
        ('Management', {
            'fields': ('host', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for Review model.
    """
    list_display = ['listing', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['listing__title', 'reviewer__username', 'comment']
    readonly_fields = ['created_at']
    list_per_page = 25
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('listing', 'reviewer')