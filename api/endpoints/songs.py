from math import ceil

from bson import errors
from bson.objectid import ObjectId
from flask import abort, jsonify
from flask.wrappers import Response
from flask_restx import Resource, reqparse
from mongoengine.queryset.visitor import Q

from api.models import SongRatings, Songs
from api.schema import song_schema

BATCH_SIZE = 100000


class SongsListResource(Resource):
    """Returns a list of songs"""

    def __init__(self, *args, **kwargs) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "page_number", type=int, default=1, required=False
        )
        self.parser.add_argument(
            "songs_per_page", type=int, default=30, required=False
        )

    def get(self) -> Response:
        args = self.parser.parse_args()

        offset = (args["page_number"] - 1) * args["songs_per_page"]

        songs = (
            Songs.objects.skip(offset)
            .limit(args["songs_per_page"])
            .batch_size(BATCH_SIZE)
        )

        total_songs = Songs.objects.batch_size(BATCH_SIZE).count()
        total_pages = ceil(total_songs / args["songs_per_page"])

        next_page_number = (
            args["page_number"] + 1
            if args["page_number"] < total_pages else None
        )
        previous_page_number = (
            args["page_number"] - 1 if args["page_number"] > 1 else None
        )
        song_data = song_schema.dump(songs, many=True)

        response = jsonify(
            dict(
                songs=song_data,
                total_songs=total_songs,
                page=args["page_number"],
                songs_per_page=args["songs_per_page"],
                next_page=next_page_number,
                previous_page=previous_page_number,
                total_pages=total_pages,
            )
        )
        response.status_code = 200
        return response


class AverageDifficultyResource(Resource):
    """Returns the average difficulty for all songs"""

    def __init__(self, *args, **kwargs) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "level", type=int,
            required=False,
            help="Please provide an integer!"
        )

    def get(self) -> Response:
        args = self.parser.parse_args()

        if args["level"] is not None:
            songs = Songs.objects(level=args["level"]).batch_size(BATCH_SIZE)
        else:
            songs = Songs.objects.all().batch_size(BATCH_SIZE)

        if args["level"] and len(songs) == 0:
            abort(404, description=f"No songs found for level {args['level']}")
        if songs.count() == 0:
            abort(404, description="No songs are available!")

        response = jsonify(
            {
                "average_difficulty": round(songs.average("difficulty"), 2),
            }
        )
        response.status_code = 200

        return response


class SongSearchResource(Resource):
    """Returns a list of songs that match the search query"""

    def __init__(self, *args, **kwargs) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "message",
            type=str,
            required=True,
            help="a 'message' parameter is required!",
        )

    def get(self) -> Response:
        args = self.parser.parse_args()

        songs = Songs.objects(
            (
                Q(title__icontains=args["message"]) |
                Q(artist__icontains=args["message"])
            )
        ).batch_size(BATCH_SIZE)

        if len(songs) == 0:
            abort(
                404,
                description=(
                    f"No songs found for the search term "
                    f"'{args['message']}'!"
                ),
            )

        song_data = song_schema.dump(songs, many=True)
        response = jsonify(dict(songs=song_data))
        response.status_code = 200
        return response


class SongRatingResource(Resource):
    """Adds a rating to a song"""

    def __init__(self, *args, **kwargs) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "song_id",
            type=str,
            required=True,
            help="a 'song_id' parameter value is required!",
        )
        self.parser.add_argument(
            "rating",
            type=int,
            required=True,
            help="a 'rating' integer parameter value is required!",
        )

    def post(self) -> Response:
        args = self.parser.parse_args()

        if 1 > args["rating"] or args["rating"] > 5:
            abort(400, description="Please provide a rating between 1 and 5!")

        try:
            song = Songs.objects(id=ObjectId(args["song_id"])).first()
        except errors.InvalidId:
            abort(
                400,
                description=(
                    f" The song id {args['song_id']} is invalid! "
                    f"it must be a 12-byte input or a 24-character hex string"
                ),
            )

        if song is None:
            abort(404, description=f"No song found with id {args['song_id']}")

        song.ratings.append(
            SongRatings(
                rating=args["rating"],
                song_id=ObjectId(args["song_id"]),
            )
        )
        song.save()

        response = jsonify(
            dict(
                message=f"New song rating added for {song.title}!",
                rating=args["rating"],
                song_id=args["song_id"],
            )
        )
        response.status_code = 201
        return response


class RatingMetricsResource(Resource):
    """Returns the average, lowest and highest rating for a song"""

    def __init__(self, *args, **kwargs) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "song_id",
            type=str,
            required=True,
            help="a 'song_id' parameter is required!",
        )

    def get(self) -> Response:
        args = self.parser.parse_args()
        try:
            song = Songs.objects(id=ObjectId(args["song_id"])).first()
        except errors.InvalidId:
            abort(
                400,
                description=(
                    f"The song id {args['song_id']} is invalid! "
                    f"it must be a 12-byte input or a 24-character hex string"
                ),
            )

        if song is None:
            abort(
                404,
                description=(
                    f"No song found for ID {args['song_id']} "
                    f"or invalid song_id provided!"
                ),
            )

        ratings = [rating.rating for rating in song.ratings]

        try:
            average_rating = round(sum(ratings) / len(ratings), 2)
        except ZeroDivisionError:
            abort(404, description="No ratings have been found for this song!")
        except TypeError:
            abort(400, description="Ratings provided aren't valid integers!")

        response = jsonify(
            dict(
                average_rating=average_rating,
                lowest_rating=min(ratings),
                highest_rating=max(ratings),
            )
        )
        response.status_code = 200
        return response
