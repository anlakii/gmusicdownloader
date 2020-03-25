from entities.artist import Artist
from entities.track import Track
from typing import List

class Album:
    def __init__(self, title: str, artist: Artist, tracklist: List[Track],
                 album_art: str):
        self.title     = title
        self.artist    = artist
        self.tracklist = tracklist
        self.album_art = album_art
