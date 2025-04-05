# LIBRARY IMPORTS


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

        self.ts = stream["ts"]
        self.platform = stream["platform"]
        self.ms_played = stream["ms_played"]
        self.conn_country = stream["conn_country"]
        self.master_metadata_track_name = stream["master_metadata_track_name"]
        self.master_metadata_album_artist_name = stream["master_metadata_album_artist_name"]
        self.master_metadata_album_album_name = stream["master_metadata_album_album_name"]
        self.spotify_track_uri = stream["spotify_track_uri"]
        self.episode_name = stream["episode_name"]
        self.episode_show_name = stream["episode_show_name"]
        self.spotify_episode_uri = stream["spotify_episode_uri"]

        self.reason_start = stream["reason_start"]
        re = stream["reason_end"].replace('-', '_')
        self.reason_end = re

# ----------------------------------------------------------------------------------------------- #
