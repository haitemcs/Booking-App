from django.db import models


class Room(models.Model):
    room_number = models.IntegerField(unique=True)

    ROOM_TYPES = [
        ("standard", "Standard"),
        ("modern", "Modern"),
        ("classic", "Classic"),
        ("suite", "Suite"),
    ]

    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"