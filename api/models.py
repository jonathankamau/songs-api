"""Song Models File"""

from mongoengine import (Document, EmbeddedDocument, EmbeddedDocumentListField,
                         FloatField, IntField, ObjectIdField, StringField)


class SongRatings(EmbeddedDocument):
    """Song Ratings Model"""

    song_id = ObjectIdField(required=True)
    rating = IntField(min_value=1, max_value=5, required=True)


class Songs(Document):
    """Song Model"""

    artist = StringField(max_length=200, required=True)
    title = StringField(max_length=200, required=True)
    difficulty = FloatField(required=True)
    level = FloatField(required=True)
    released = StringField(max_length=200, required=True)
    ratings = EmbeddedDocumentListField(SongRatings, required=False)
