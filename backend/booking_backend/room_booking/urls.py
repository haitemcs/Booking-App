from django.urls import path
from room_booking import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", views.api_root, name="api-root"),
    path("rooms/", views.RoomList.as_view(), name="room-list"),
]

