from django.contrib import admin

from .models import Room, RoomImage, occupancy

admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(occupancy)
