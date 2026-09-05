from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['url', 'room_number', 'room_type', 'price_per_night', 'currency', 'description', 'is_available']