# LIBRARY IMPORTS
from datetime import datetime

# LOCAL IMPORTS


# ----------------------------------------------------------------------------------------------- #

class Stream:
    """
    Takes stream information and makes a stream object.
    """

    # ----------------------------------------------------------------------------------------------- #

    def __init__(self, stream):
        """
        Constructor for the stream object
        """

        dt = datetime.strptime(stream["ts"], "%Y-%m-%dT%H:%M:%SZ")
        ts = dt.strftime("%Y-%m-%d %H:%M:%S")
        self.ts = ts
        self.platform = stream["platform"]
        ms = int(stream["ms_played"]) / 1000 # convertion from ms to seconds, 60000 for mins
        self.ms_played = ms
        self.conn_country = stream["conn_country"]
        self.master_metadata_track_name = stream["master_metadata_track_name"]
        self.master_metadata_album_artist_name = stream["master_metadata_album_artist_name"]
        self.master_metadata_album_album_name = stream["master_metadata_album_album_name"]
        self.spotify_track_uri = stream["spotify_track_uri"]
        self.episode_name = stream["episode_name"]
        self.episode_show_name = stream["episode_show_name"]
        self.spotify_episode_uri = stream["spotify_episode_uri"]
        rs = stream["reason_start"].replace('-', '_')
        self.reason_start = rs
        re = stream["reason_end"].replace('-', '_')
        self.reason_end = re

# ----------------------------------------------------------------------------------------------- #
