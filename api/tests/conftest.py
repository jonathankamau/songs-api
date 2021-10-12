import pytest

from api.models import SongRatings, Songs
from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    yield
    Songs.objects.delete()


@pytest.fixture()
def song():
    return Songs.objects.first()


@pytest.fixture(scope="function")
def ratings(song):
    ratings = [
        {"song_id": song.id, "rating": 1},
        {"song_id": song.id, "rating": 2},
        {"song_id": song.id, "rating": 3},
        {"song_id": song.id, "rating": 4},
        {"song_id": song.id, "rating": 5},
    ]
    rating_instances = [SongRatings(**rating) for rating in ratings]

    song.ratings = rating_instances
    song.save()
