from rest_framework import serializers
from .models import Spot, SpotImage, SpotCategory
from reviews.models import Review

class SpotCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotCategory
        fields = ['id', 'name', 'description']

class SpotImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotImage
        fields = ['id', 'spot', 'image']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'username', 'content', 'rating', 'created_at']

class SpotSerializer(serializers.ModelSerializer):
    images = SpotImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Spot
        fields = [
            'id', 'title', 'description', 'address', 
            'category', 'category_name', 'created_by_username', 'created_at', 
            'total_likes', 'images', 'reviews'
        ]

    def get_category_name(self, obj):
        return obj.get_category_display()
