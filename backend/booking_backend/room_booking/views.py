from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.exceptions import PermissionDenied

from .models import Room, RoomImage, Occupancy
from .serializers import RoomSerializer, RoomImageSerializer, OccupancySerializer, UserSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(request.user and request.user.is_staff)


class LoginRateThrottle(ScopedRateThrottle):
    scope = "login"


class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.prefetch_related("images")
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.prefetch_related("images")
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomImageList(generics.ListCreateAPIView):
    queryset = RoomImage.objects.select_related("room")
    serializer_class = RoomImageSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoomImage.objects.select_related("room")
    serializer_class = RoomImageSerializer
    permission_classes = [IsAdminOrReadOnly]


class OccupancyList(generics.ListCreateAPIView):
    serializer_class = OccupancySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Occupancy.objects.select_related("room", "user").order_by("start_date")
        if user.is_superuser or user.is_staff:
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(user=self.request.user)


class OccupancyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OccupancySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Occupancy.objects.select_related("room", "user")
        if user.is_superuser or user.is_staff:
            return qs
        return qs.filter(user=user)


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj == user or user.is_staff or user.is_superuser:
            return obj
        raise PermissionDenied("You do not have permission to access this profile.")


def issue_token(user):
    # Rotate the credential so a successful login invalidates any previously
    # issued token for this account.
    Token.objects.filter(user=user).delete()
    return Token.objects.create(user=user)


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data["id"])
        token = issue_token(user)
        response.data = {
            "user": {"id": user.id, "username": user.username, "email": user.email,
                     "first_name": user.first_name, "last_name": user.last_name},
            "token": token.key,
        }
        return response


class Login(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "")
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        token = issue_token(user)
        return Response({
            "token": token.key,
            "user": {"id": user.id, "username": user.username, "email": user.email,
                     "first_name": user.first_name, "last_name": user.last_name},
        })


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Logged out."})


@api_view(["GET"])
@permissions.permission_classes([permissions.AllowAny])
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
