from rest_framework import serializers
from .models import Room , RoomImage , occupancy


class RoomImageSerializer(serializers.ModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        view_name='room-detail', 
        queryset=Room.objects.all()    
    )
    class Meta:
        model = RoomImage 
        fields = ['id', 'image', 'caption' , 'room']




class RoomSerializer(serializers.HyperlinkedModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Room
        fields = ['url', 'room_number', 'room_type', 'price_per_night', 'currency', 'description', 'is_available', 'images'    ]



class OccupancySerializer(serializers.ModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        view_name='room-detail', 
        queryset=Room.objects.all()    
    )
    class Meta:
        model = occupancy
        fields = ['url' , 'id', 'room', 'start_date', 'end_date']
