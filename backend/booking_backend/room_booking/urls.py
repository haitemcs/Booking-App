from django.urls import path
from room_booking import views
from rest_framework.urlpatterns import format_suffix_patterns, include


urlpatterns = [
    path("", views.api_root, name="api-root"),
    path("rooms/", views.RoomList.as_view(), name="room-list"),
    path("rooms/<int:pk>/", views.RoomDetail.as_view(), name="room-detail"),
    path("room-images/", views.RoomImageList.as_view(), name="roomimage-list"),
    path("room-images/<int:pk>/", views.RoomImageDetail.as_view(), name="roomimage-detail"),
    path("occupancies/", views.OccupancyList.as_view(), name="occupancy-list"),
    path("occupancies/<int:pk>/", views.OccupancyDetail.as_view(), name="occupancy-detail"),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


