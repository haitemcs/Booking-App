from rest_framework.response import Response
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from .models import Room, RoomImage, occupancy
from .serializers import OccupancySerializer, RoomImageSerializer, RoomSerializer

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer 

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomImageList(generics.ListCreateAPIView):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer

class RoomImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageSerializer

class occupancyList(generics.ListCreateAPIView):
    queryset = occupancy.objects.all()
    serializer_class = OccupancySerializer

class OccupancyDateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = occupancy.objects.all()
    serializer_class = OccupancySerializer    


@api_view(["GET"])

def api_root(request, format=None):
    return Response({
        "rooms": reverse("room-list", request=request, format=format)
    })


