class TestRetrieveSongs:
    def test_get_songs_with_pagination(self, client):
        response = client.get("/api/v1/songs?page_number=2&songs_per_page=2")

        response_data = response.json
        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert response_data["songs"] == [
            {
                "artist": "Mr Fastfinger",
                "difficulty": 15,
                "level": 13,
                "released": "2012-05-11",
                "title": "Awaki-Waki",
            },
            {
                "artist": "The Yousicians",
                "difficulty": 13.22,
                "level": 13,
                "released": "2014-12-20",
                "title": "You've Got The Power",
            },
        ]
        assert len(response_data["songs"]) == 2
        assert response_data["songs_per_page"] == 2
        assert response_data["page"] == 2
        assert response_data["previous_page"] == 1
        assert response_data["next_page"] == 3

    def test_get_songs_without_pagination(self, client):
        response = client.get("/api/v1/songs")
        response_data = response.json
        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert len(response_data["songs"]) == 11
        assert response_data["songs_per_page"] == 30
        assert not response_data["previous_page"]
        assert not response_data["next_page"]
