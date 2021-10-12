class TestSongSearch:
    def test_search_songs_by_title(self, client):
        response = client.get("/api/v1/songs/search?message=Awaki-Waki")
        response_data = response.json
        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert len(response_data["songs"]) == 1
        assert response_data["songs"][0]["title"] == "Awaki-Waki"

    def test_search_songs_by_artist(self, client):
        response = client.get("/api/v1/songs/search?message=Mr Fastfinger")
        response_data = response.json
        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert len(response_data["songs"]) == 1
        assert response_data["songs"][0]["artist"] == "Mr Fastfinger"

    def test_search_songs_without_message_parameter(self, client):
        response = client.get("/api/v1/songs/search")
        response_data = response.json
        assert response.status_code == 400
        assert (
            "a 'message' parameter is required"
            in response_data["errors"]["message"]
        )

    def test_search_songs_with_invalid_message_parameter(self, client):
        response = client.get("/api/v1/songs/search?message=Mike")
        response_data = response.json
        assert response.status_code == 404
        assert (
            "No songs found for the search term 'Mike'"
            in response_data["message"]
        )
