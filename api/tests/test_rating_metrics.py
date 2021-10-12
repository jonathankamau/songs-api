class TestRatingMetrics:
    def test_rating_metrics(
        self,
        client,
        song,
        ratings,
    ):
        response = client.get(
            f"/api/v1/songs/rating/metrics?song_id={str(song.id)}"
        )
        assert response.status_code == 200
        assert response.json == {
            "average_rating": 3.0,
            "lowest_rating": 1,
            "highest_rating": 5,
        }

    def test_rating_metrics_no_song(
        self,
        client,
        song,
        ratings,
    ):
        song_id = "6161cd1d249469d134326644"
        response = client.get(
            f"/api/v1/songs/rating/metrics?song_id={song_id}"
        )
        assert response.status_code == 404
        response_data = response.json
        assert (
            f"No song found for ID {song_id} or invalid song_id provided!"
            in response_data["message"]
        )

    def test_rating_metrics_invalid_song_id(
        self,
        client,
        song,
        ratings,
    ):
        song_id = "123"
        response = client.get(
            f"/api/v1/songs/rating/metrics?song_id={song_id}"
        )
        assert response.status_code == 400
        response_data = response.json
        assert f"The song id {song_id} is invalid!" in response_data["message"]

    def test_rating_metrics_missing_ratings(self, client, song):
        response = client.get(
            f"/api/v1/songs/rating/metrics?song_id={str(song.id)}"
        )
        assert response.status_code == 404
        response_data = response.json
        assert (
            "No ratings have been found for this song!"
            in response_data["message"]
        )
