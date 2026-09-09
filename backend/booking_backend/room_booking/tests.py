from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Occupancy, Room


class BookingApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="StrongPass123!")
        self.other = User.objects.create_user(username="bob", password="StrongPass123!")
        self.room = Room.objects.create(room_number=101, room_type="standard", price_per_night="100.00", currency="USD")
        self.rooms_url = reverse("room-list")
        self.occupancies_url = reverse("occupancy-list")
        self.today = timezone.localdate()

    def authenticate(self, user=None):
        token = Token.objects.get_or_create(user=user or self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def room_url(self):
        return f"http://testserver{reverse('room-detail', args=[self.room.id])}"

    def test_token_authentication_works(self):
        self.authenticate()
        response = self.client.get(self.occupancies_url)
        self.assertEqual(response.status_code, 200)

    def test_normal_user_cannot_modify_rooms(self):
        self.authenticate()
        response = self.client.post(self.rooms_url, {
            "room_number": 102, "room_type": "standard", "price_per_night": "80.00", "currency": "USD"
        }, format="json")
        self.assertEqual(response.status_code, 403)

    def test_booking_uses_authenticated_user(self):
        self.authenticate()
        response = self.client.post(self.occupancies_url, {
            "room": self.room_url(),
            "start_date": str(self.today + timedelta(days=2)),
            "end_date": str(self.today + timedelta(days=4)),
        }, format="json")
        self.assertEqual(response.status_code, 201)
        booking = Occupancy.objects.get(id=response.data["id"])
        self.assertEqual(booking.user, self.user)

    def test_overlapping_booking_is_rejected(self):
        Occupancy.objects.create(room=self.room, user=self.user,
                                 start_date=self.today + timedelta(days=2),
                                 end_date=self.today + timedelta(days=5))
        self.authenticate(self.other)
        response = self.client.post(self.occupancies_url, {
            "room": self.room_url(),
            "start_date": str(self.today + timedelta(days=4)),
            "end_date": str(self.today + timedelta(days=6)),
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("already booked", str(response.data))

    def test_user_sees_only_own_bookings(self):
        Occupancy.objects.create(room=self.room, user=self.other,
                                 start_date=self.today + timedelta(days=2),
                                 end_date=self.today + timedelta(days=3))
        self.authenticate(self.user)
        response = self.client.get(self.occupancies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_invalid_date_range_is_rejected(self):
        self.authenticate()
        response = self.client.post(self.occupancies_url, {
            "room": self.room_url(),
            "start_date": str(self.today + timedelta(days=5)),
            "end_date": str(self.today + timedelta(days=5)),
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_register_returns_token(self):
        response = self.client.post(reverse("register"), {
            "username": "new-user", "email": "new@example.com", "password": "StrongPass123!"
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["token"])
