from rest_framework.response import Response
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from .models import Room
from .serializers import RoomSerializer

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer 



@api_view(["GET"])
    
def api_root(request, format=None):
    return Response({
        "rooms": reverse("room-list", request=request, format=format)
    })

