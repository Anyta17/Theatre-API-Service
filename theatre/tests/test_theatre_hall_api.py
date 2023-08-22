from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from theatre.models import TheatreHall
from theatre.serializers import TheatreHallSerializer
from unittest import TestCase

HALL_URL = reverse("theatre:theatrehall-list")


class UnauthenticatedTheatreHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(HALL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTheatreHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, _ = get_user_model().objects.get_or_create(
            email="test@email.com",
            defaults={"password": "password"}
        )
        self.client.force_authenticate(self.user)

    def test_list_theatre_halls(self):
        TheatreHall.objects.create(name="Hall A", rows=10, seats_in_row=10)
        TheatreHall.objects.create(name="Hall B", rows=8, seats_in_row=12)

        res = self.client.get(HALL_URL)
        halls = TheatreHall.objects.all()
        serializer = TheatreHallSerializer(halls, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_theatre_hall_forbidden(self):
        payload = {
            "name": "Hall C",
            "rows": 7,
            "seats_in_row": 14,
        }

        res = self.client.post(HALL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTheatreHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, _ = get_user_model().objects.get_or_create(
            email="admin@admin.com",
            defaults={"password": "testpassword"},
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_theatre_hall_created(self):
        payload = {
            "name": "Hall D",
            "rows": 6,
            "seats_in_row": 15,
        }

        res = self.client.post(HALL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
