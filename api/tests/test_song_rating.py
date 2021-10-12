import pytest


class TestSongRating:
    def test_add_song_rating(
        self,
        client,
        song,
    ):
        rating = 3
        response = client.post(
            f"/api/v1/songs/rating?song_id={str(song.id)}&rating={rating}",
        )
        assert response.status_code == 201
        response_data = response.json
        assert response_data["message"] == (
            f"New song rating added for {song.title}!"
        )
        assert response_data["song_id"] == str(song.id)
        assert response_data["rating"] == rating

    def test_add_song_rating_invalid_song_id(
        self,
        client,
    ):
        rating = 3
        song_id = "123"
        response = client.post(
            f"/api/v1/songs/rating?song_id={song_id}&rating={rating}",
        )
        assert response.status_code == 400
        response_data = response.json
        assert f"The song id {song_id} is invalid!" in response_data["message"]

    def test_add_song_rating_no_matching_song(self, client):
        rating = 4
        song_id = "6161cd1d249469d134326644"
        response = client.post(
            f"/api/v1/songs/rating?song_id={song_id}&rating={rating}",
        )
        assert response.status_code == 404
        response_data = response.json
        assert f"No song found with id {song_id}" in response_data["message"]

    @pytest.mark.parametrize(
        "rating",
        [
            "0",
            "-1",
            "9",
        ],
    )
    def test_add_song_rating_invalid_rating(
        self,
        client,
        song,
        rating,
    ):
        response = client.post(
            f"/api/v1/songs/rating?song_id={str(song.id)}&rating={rating}",
        )
        assert response.status_code == 400
        response_data = response.json
        assert response_data["message"] == (
            "Please provide a rating between 1 and 5!"
        )
