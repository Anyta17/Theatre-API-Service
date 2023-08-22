from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Genre, Actor, Play
from theatre.serializers import PlayListSerializer, PlayDetailSerializer

PLAY_URL = reverse("theatre:play-list")


def detail_url(play_id: int):
    return reverse("theatre:play-detail", args=[play_id])


def sample_play(**params):
    defaults = {
        "title": "Natalka Poltavka",
        "description": "Description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user, _ = get_user_model().objects.get_or_create(
            email="test@email.com",
            defaults={"password": "password"}
        )
        self.client.force_authenticate(self.user)

        self.genre, _ = Genre.objects.get_or_create(name="novel")

    def test_list_plays(self):
        sample_play()
        theatre_with_genre = sample_play()
        theatre_with_actor = sample_play()

        actor = Actor.objects.create(first_name="Ada", last_name="Maas")

        theatre_with_genre.genres.add(self.genre)
        theatre_with_actor.actors.add(actor)

        res = self.client.get(PLAY_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_plays_by_genres_and_actors(self):
        theatre1 = sample_play(title="Theatre 1")

        actor1 = Actor.objects.create(first_name="name", last_name="test")

        theatre1.genres.add(self.genre)
        theatre1.actors.add(actor1)

        theatre2 = sample_play(title="Theatre without genres")

        res = self.client.get(PLAY_URL, {"genres": f"{self.genre.id}", "actors": f"{actor1.id}"})

        serializer1 = PlayListSerializer(theatre1)
        serializer2 = PlayListSerializer(theatre2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_play_detail(self):
        play = sample_play()
        play.genres.add(self.genre)
        play.actors.add(Actor.objects.create(first_name="Nick", last_name="Black"))

        url = detail_url(play.id)
        res = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_play_forbidden(self):
        payload = {
            "title": "Romeo & Juliet",
            "description": "test",
        }

        res = self.client.post(PLAY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user, _ = get_user_model().objects.get_or_create(
            email="admin@addmin.com",
            defaults={"password": "testpassword"},
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

        self.genre, _ = Genre.objects.get_or_create(name="novel")
        self.actor = Actor.objects.create(first_name="John", last_name="Dg")

    def test_theatre_created(self):
        payload = {
            "title": "Calvary",
            "description": "test",
            "genres": [self.genre.id],
            "actors": [self.actor.id]
        }

        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
