""" Schema file. """
from marshmallow import Schema, fields


class SongSchema(Schema):
    """ Schema for the Song model """

    title = fields.Str(required=True)
    artist = fields.Str(required=True)
    difficulty = fields.Float(required=True)
    level = fields.Float(required=True)
    released = fields.Str(required=True)


song_schema = SongSchema()
