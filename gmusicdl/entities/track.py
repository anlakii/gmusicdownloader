from entities.artist import Artist
from typing import Callable

class Track:
    def __init__(self, title: str, artist: Artist):
        this.title  = title
        this.artist = artist

    def __init__(self, title: str, artist: Artist, dl_url: str, callback: Callable):
        this.title    = title
        this.artist   = artist
        this.dl_url   = dl_url
        this.callback = callback
