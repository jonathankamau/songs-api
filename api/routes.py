""" Resource routes for the API """
from api.endpoints.songs import (AverageDifficultyResource,
                                 RatingMetricsResource, SongRatingResource,
                                 SongSearchResource, SongsListResource)


def resource_routes(api):
    """ Define the routes for the API """
    api.add_resource(
        SongsListResource,
        "/api/v1/songs",
        endpoint="song"
    )

    api.add_resource(
        AverageDifficultyResource,
        "/api/v1/songs/difficulty",
        endpoint="difficulty"
    )

    api.add_resource(
        SongSearchResource,
        "/api/v1/songs/search",
        endpoint="search"
    )

    api.add_resource(
        SongRatingResource,
        "/api/v1/songs/rating",
        endpoint="rating"
    )

    api.add_resource(
        RatingMetricsResource,
        "/api/v1/songs/rating/metrics",
        endpoint="metric"
    )
