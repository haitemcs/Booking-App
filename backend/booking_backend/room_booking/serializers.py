from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from .models import Room, RoomImage, Occupancy


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            password_validation.validate_password(password, instance)
            instance.set_password(password)
        instance.save()
        return instance


class RoomImageSerializer(serializers.ModelSerializer):
    room = serializers.HyperlinkedRelatedField(view_name="room-detail", queryset=Room.objects.all())

    class Meta:
        model = RoomImage
        fields = ["id", "image", "caption", "room"]


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["url", "room_number", "room_type", "price_per_night", "currency", "description", "is_available", "images"]

    def validate_price_per_night(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_currency(self, value):
        return value.upper()


class OccupancySerializer(serializers.ModelSerializer):
    room = serializers.HyperlinkedRelatedField(view_name="room-detail", queryset=Room.objects.all())

    class Meta:
        model = Occupancy
        fields = ["id", "room", "start_date", "end_date"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        room = attrs.get("room", getattr(self.instance, "room", None))

        if not start or not end:
            raise serializers.ValidationError("Check-in and check-out dates are required.")
        if end <= start:
            raise serializers.ValidationError({"end_date": "Check-out must be after check-in."})
        if start < timezone.localdate():
            raise serializers.ValidationError({"start_date": "Check-in cannot be in the past."})
        if room and not room.is_available:
            raise serializers.ValidationError({"room": "This room is not available for booking."})

        overlapping = Occupancy.objects.filter(room=room, start_date__lt=end, end_date__gt=start)
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)
        if overlapping.exists():
            raise serializers.ValidationError("This room is already booked for part of those dates.")
        return attrs
