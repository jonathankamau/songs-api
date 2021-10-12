class TestSongAverageDifficulty:
    def test_average_difficulty_of_all_songs(self, client):
        response = client.get("/api/v1/songs/difficulty")
        response_data = response.json
        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert response_data["average_difficulty"] == 10.32

    def test_average_difficulty_of_selected_songs(self, client):
        response = client.get("/api/v1/songs/difficulty?level=9")
        response_data = response.json
        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert response_data["average_difficulty"] == 9.69

    def test_average_difficulty_invalid_parameter_value(self, client):
        response = client.get("/api/v1/songs/difficulty?level=fsdfdsfsdf")
        response_data = response.json
        assert response.status_code == 400
        assert response_data["message"] == "Input payload validation failed"

    def test_average_difficulty_no_songs_found_for_level(self, client):
        response = client.get("/api/v1/songs/difficulty?level=100")
        response_data = response.json
        assert response.status_code == 404
        assert "No songs found for level 100" in response_data["message"]
