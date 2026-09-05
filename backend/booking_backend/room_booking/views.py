from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Room, RoomImage, Occupancy
from .serializers import RoomSerializer, RoomImageSerializer, OccupancySerializer, UserSerializer


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


class OccupancyList(generics.ListCreateAPIView):
    serializer_class = OccupancySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Occupancy.objects.all()
        return Occupancy.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OccupancyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Occupancy.objects.all()
    serializer_class = OccupancySerializer
    permission_classes = [IsAuthenticated]


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj == user or user.is_staff or user.is_superuser:
            return obj
        raise PermissionDenied("You do not have permission to view this profile.")


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])
        token, created = Token.objects.get_or_create(user=user)
        response.data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'token': token.key,
        }
        return response


class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({'detail': 'Logged out.'})


@api_view(["GET"])

def api_root(request, format=None):
    return Response({
        "rooms": reverse("room-list", request=request, format=format),
        "room-images": reverse("roomimage-list", request=request, format=format),
        "occupancies": reverse("occupancy-list", request=request, format=format),
        "users": reverse("user-list", request=request, format=format),
        "register": reverse("register", request=request, format=format),
        "login": reverse("login", request=request, format=format),
        "logout": reverse("logout", request=request, format=format),
    })