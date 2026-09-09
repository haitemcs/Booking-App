from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Room(models.Model):
    room_number = models.IntegerField(unique=True)
    ROOM_TYPES = [("standard", "Standard"), ("modern", "Modern"), ("classic", "Classic"), ("suite", "Suite")]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="room_images/")
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for Room {self.room.room_number}"


class Occupancy(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="occupancies")
    # Nullable for compatibility with the original migration's legacy rows.
    # New bookings are always assigned to request.user by the API.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="occupancies", null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [models.CheckConstraint(condition=Q(end_date__gt=models.F("start_date")), name="occupancy_end_after_start")]
        indexes = [
            models.Index(fields=["room", "start_date", "end_date"]),
            models.Index(fields=["user", "start_date"]),
        ]

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError({"end_date": "Check-out must be after check-in."})

    def __str__(self):
        return f"Occupancy for Room {self.room.room_number} from {self.start_date} to {self.end_date}"
