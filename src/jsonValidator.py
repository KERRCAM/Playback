# LIBRARY IMPORTS
import os
from os import listdir
from os.path import isfile, join


# LOCAL IMPORTS


# -------------------------------------------------------------------------- #

class JsonValidator:
    """
    Takes input of the uploaded folder name and checks if all the JSON
    files in the folder are in the expected and correct format.

    Returns either all files are valid or returns any issues with the files.

    Example returns for issues include:
    - No json files present in the folder
    - Unexpected JSON file name
    - Invalid JSON structure in file X at line X - (REASON)

    Expected file name formats:
    "Streaming_History_Audio_YYYY.json"
    "Streaming_History_Audio_YYYY_X.json"
    "Streaming_History_Audio_YYYY-YYYY.json"
    "Streaming_History_Audio_YYYY-YYYY_X.json"

    Expected JSON structure:
    List of elements each related to an individual stream
    [
        {
            "ts": "YYYY-MM-DDThh:mm:ssZ",
            "platform": "Any string",
            "ms_played": 0+,
            "conn_country": "XX",
            "ip_addr": "IGNORED",
            "master_metadata_track_name": "Any string or null",
            "master_metadata_album_artist_name": "Any string or null",
            "master_metadata_album_album_name": "Any string or null",
            "spotify_track_uri": "spotify:track:CODE",
            "episode_name": "Any string or null",
            "episode_show_name": "Any string or null",
            "spotify_episode_uri": "Any string or null",
            "reason_start": "trackdone" OR "fwdbtn" OR "backbtn" OR "clickrow",
            "reason_end": "trackdone" OR "fwdbtn" OR "backbtn" OR "remote" OR "endplay",
            "shuffle": true OR false,
            "skipped": true OR false,
            "offline": true OR false,
            "offline_timestamp": 1683231370,
            "incognito_mode": true OR false
        },
        ....
    ]
    Note: if song name information null episode should not and vice versa.
    """

# -------------------------------------------------------------------------- #

    def __init__(self, folderName):
        """
        Constructor takes input of uploaded folder name
        """

        self.folderName = folderName
        self.fileNames = self.getFiles(folderName)

        print(self.fileNames)

    # ---------------------------------------------------------------------- #

    def getFiles(self, dir):
        """
        Gets all the JSON files names given in the uploaded folder
        :return: returns a list of the JSON files as strings
        """

        dir_path = os.path.dirname(os.path.realpath(__file__))
        fileNames = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

        return fileNames

    # ---------------------------------------------------------------------- #

    def charAdvance(self, ):
        """
        moves curr char pointer to next char in input
        """

        pass

    # ---------------------------------------------------------------------- #

    def consumeDateTime(self, ):
        """

        """

        pass

    # ---------------------------------------------------------------------- #

    def consumeNumber(self, ):
        """

        """

        pass

    # ---------------------------------------------------------------------- #

    def consumeString(self, ):
        """

        """

        pass

    # ---------------------------------------------------------------------- #

    def consumeValue(self, ):
        """

        """

        pass

    # ---------------------------------------------------------------------- #

    def consumeList(self, ):
        """

        """

        pass

    # ---------------------------------------------------------------------- #

    def validateFile(self, ):
        """

        """

        pass

    # ---------------------------------------------------------------------- #


# FOR TESTING ONLY
def main():
    v = JsonValidator("src")

if __name__ == "__main__":
    main()