from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 
            'location', 'event_type', 'related_spot', 
            'created_by_username', 'discount_percentage', 
            'contact_info', 'created_at', 'is_active'
        ]
