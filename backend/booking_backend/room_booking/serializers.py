from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Room, RoomImage, Occupancy


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RoomImageSerializer(serializers.ModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        view_name='room-detail',
        queryset=Room.objects.all()
    )

    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'caption', 'room']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['url', 'room_number', 'room_type', 'price_per_night', 'currency', 'description', 'is_available', 'images']


class OccupancySerializer(serializers.ModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        view_name='room-detail',
        queryset=Room.objects.all()
    )

    class Meta:
        model = Occupancy
        fields = ['id', 'room', 'start_date', 'end_date']
