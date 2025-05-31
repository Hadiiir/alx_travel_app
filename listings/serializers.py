"""
Serializers for the listings app.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Review


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    """
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model.
    """
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'property_type', 'price_per_night',
            'location', 'latitude', 'longitude', 'max_guests', 'bedrooms',
            'bathrooms', 'amenities', 'host', 'is_active', 'created_at',
            'updated_at', 'reviews', 'average_rating', 'review_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        """Calculate average rating for the listing."""
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def get_review_count(self, obj):
        """Get total number of reviews for the listing."""
        return obj.reviews.count()


class ListingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new listings.
    """
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'property_type', 'price_per_night',
            'location', 'latitude', 'longitude', 'max_guests', 'bedrooms',
            'bathrooms', 'amenities'
        ]
    
    def create(self, validated_data):
        """Create a new listing with the current user as host."""
        validated_data['host'] = self.context['request'].user
        return super().create(validated_data)