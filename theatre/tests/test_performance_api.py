from datetime import datetime
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from theatre.models import TheatreHall, Performance
from theatre.serializers import PerformanceSerializer, PerformanceListSerializer
from unittest import TestCase

from theatre.tests.test_play_api import sample_play

PERFORMANCE_URL = reverse("theatre:performance-list")


def detail_url(performance_id: int):
    return reverse("theatre:performance-detail", args=[performance_id])


def sample_hall(**params):
    defaults = {
        "name": "Hall A",
        "rows": 15,
        "seats_in_row": 10
    }
    defaults.update(params)

    return TheatreHall.objects.create(**defaults)


def sample_performance(**params):
    defaults = {
        "play": sample_play(),
        "theatre_hall": sample_hall(),
        "show_time": datetime.now(),
    }
    defaults.update(params)
    return Performance.objects.create(**defaults)


class AuthenticatedPerformanceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, _ = get_user_model().objects.get_or_create(
            email="test@email.com",
            defaults={"password": "password"}
        )
        self.client.force_authenticate(self.user)

    def test_list_performances(self):
        sample_performance()
        sample_performance()
        res = self.client.get(PERFORMANCE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_performance_detail(self):
        performance = sample_performance()
        url = detail_url(performance.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AdminPerformanceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user, _ = get_user_model().objects.get_or_create(
            email="admin@admin.com",
            defaults={"password": "testpassword"},
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_performance_created(self):
        play = sample_play()
        hall = sample_hall()
        payload = {
            "play": play.id,
            "theatre_hall": hall.id,
            "show_time": datetime.now(),
        }
        res = self.client.post(PERFORMANCE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
