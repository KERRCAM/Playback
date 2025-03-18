# LIBRARY IMPORTS
import os
import sys
from importlib.resources import contents
from os import listdir
from os.path import isfile, join
from platform import system


# LOCAL IMPORTS


# ----------------------------------------------------------------------------------------------- #

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

# ----------------------------------------------------------------------------------------------- #

    def __init__(self, folderName):
        """
        Constructor takes input of uploaded folder name
        """

        fileNames, dirPath = self.getFiles(folderName)
        #fileNames = self.validateFileNames(fileNames)
        self.validateFiles(fileNames, dirPath)





    # ------------------------------------------------------------------------------------------- #

    @staticmethod
    def getFiles(folderName): # not used rn but will be needed when a folder is uploaded
        """
        Gets all the JSON files names given in the uploaded folder
        :return: returns a list of the JSON files as strings
        """

        filePath = os.path.dirname(os.path.realpath(__file__))
        if system() == "Windows":
            dirPath = os.path.relpath("..\\testFiles", filePath)
        else:
            dirPath = os.path.relpath("../testFiles" ,filePath)
        fileNames = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]

        jsonFiles = []
        for file in fileNames:
            if file[-5:] == ".json":
                jsonFiles.append(file)

        return jsonFiles, dirPath

    # ------------------------------------------------------------------------------------------- #

    def charAdvance(self):
        """
        moves curr char pointer to next char in input
        """

        self.pos += 1
        self.currChar = self.currContents[self.pos]

    # ------------------------------------------------------------------------------------------- #

    def consumeDateTime(self, ):
        """

        """

        pass

    # ------------------------------------------------------------------------------------------- #

    def consumeNumber(self, ):
        """

        """

        pass

    # ------------------------------------------------------------------------------------------- #

    def consumeString(self, ):
        """

        """

        pass

    # ------------------------------------------------------------------------------------------- #

    def consumeValue(self, ):
        """

        """

        pass

    # ------------------------------------------------------------------------------------------- #

    def consumeObject(self, ):
        """

        """

        pass

    # ------------------------------------------------------------------------------------------- #

    def consumeArray(self, ):
        """

        """

        pass

    # ------------------------------------------------------------------------------------------- #

    def validateFileNames(self, fileNames):
        """
        REWRITE
        Expected file name formats:
        "Streaming_History_Audio_YYYY.json"
        "Streaming_History_Audio_YYYY_X.json"
        "Streaming_History_Audio_YYYY-YYYY.json"
        "Streaming_History_Audio_YYYY-YYYY_X.json"
        """

        validFileNames = []

        # temporary - only checks for json files rn
        for file in reversed(fileNames):
            if not file.endswith(".json"):
                fileNames.remove(file)

        return validFileNames

    # ------------------------------------------------------------------------------------------- #

    def validateFile(self, fileName):
        """

        """



        # read file - probably buffered?

        with open(fileName, 'r') as file:
            file_content = ''
            line = file.readline()

            while line:
                file_content += line
                line = file.readline()

        print(sys.getsizeof(file_content))

    # ------------------------------------------------------------------------------------------- #

    def validateFiles(self, fileNames, dirPath):
        """
        include handing for return
        """

        for file in fileNames:
            if system() == "Windows":
                self.validateFile(dirPath + "\\\\" + file)
            else:
                self.validateFile(dirPath + "/" +file)

    # ------------------------------------------------------------------------------------------- #


# FOR TESTING ONLY
def main():
    v = JsonValidator("testFiles")

if __name__ == "__main__":
    main()