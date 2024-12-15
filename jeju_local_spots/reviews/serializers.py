from rest_framework import serializers
from .models import Review
from spots.models import Spot

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    spot_title = serializers.ReadOnlyField(source='spot.title')

    class Meta:
        model = Review
        fields = ['id', 'spot', 'spot_title', 'user', 'username', 'content', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']
