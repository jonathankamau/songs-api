import json
from itertools import chain, islice


def generate_song_data(songs_file):
    """Reads the songs file and returns song data."""
    for song_data in songs_file:
        yield json.loads(song_data)


def chunks(iterable, chunk_size=1000):
    """Yield successive n-sized chunks."""
    iterator = iter(iterable)
    for i in iterator:
        yield chain([i], islice(iterator, chunk_size - 1))
