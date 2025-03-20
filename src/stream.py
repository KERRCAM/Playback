# LIBRARY IMPORTS


# LOCAL IMPORTS


# ----------------------------------------------------------------------------------------------- #

class Stream:
    """
    Takes stream information and makes a stream object.
    """

    # ----------------------------------------------------------------------------------------------- #

    def __init__(self, ts, platform, msPlayed, country, song, artist, album,
                                    episode, show, URI, reasonStart, reasonEnd):
        """
        Constructor for the stream object
        """

        self.ts = ts
        self.platform = platform
        self.msPlayed = msPlayed
        self.country = country
        self.song = song
        self.artist = artist
        self.album = album
        self.episode = episode
        self.show = show
        self.URI = URI
        self.reasonStart = reasonStart
        self.reasonEnd = reasonEnd

# ----------------------------------------------------------------------------------------------- #