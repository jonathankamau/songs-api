import json
import os

from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_restx import Api, reqparse

from api.models import Songs
from api.routes import resource_routes
from api.utils.chunks import chunks, generate_song_data


def create_app():
    """Factory Method that creates an instance of the app with the given config.
    Args:
        environment (str): Specify the configuration to initilize app with.
    Returns:
        app (Flask): it returns an instance of Flask.
    """

    app = Flask(__name__)
    db = MongoEngine()
    app.config["MONGODB_SETTINGS"] = {
        "db": os.environ["MONGODB_DBNAME"],
        "host": os.environ["MONGODB_URI"],
    }
    db.init_app(app)

    if Songs.objects.count() == 0:
        songs_file = open("songs.json")

        song_instances = []
        for songs in chunks(generate_song_data(songs_file)):
            song_instances += [Songs(**song) for song in list(songs)]

        Songs.objects.insert(song_instances, load_bulk=True)

    api = Api(
        app=app,
        default="Api",
        default_label="Song Endpoints",
        title="Songs API",
        version="1.0.0",
        description="""Song API Documentation 📚""",
    )

    # Resources

    resource_routes(api)

    # handle default 404 exceptions
    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify(
            dict(
                error="Not found",
                message="The requested URL was not found on the server.",
            )
        )
        response.status_code = 404
        return response

    # handle default 500 exceptions
    @app.errorhandler(500)
    def internal_server_error(error):
        response = jsonify(
            dict(
                error="Internal server error",
                message="The server encountered an internal error.",
            )
        )
        response.status_code = 500
        return response

    return app
