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

    Disclaimer: Portion of this class is translated and modified version of a json validator I
    have written in C and is a public repository on my GitHub profile - Kerr Cameron
    """

# ----------------------------------------------------------------------------------------------- #

    def __init__(self, folderName):
        """
        Constructor takes input of uploaded folder name
        """

        fileNames, dirPath = self.getFiles(folderName)
        #fileNames = self.validateFileNames(fileNames)
        validFiles = self.validateFiles(fileNames, dirPath)

        self.pos = 0
        self.currChar = None
        self.currContents = None
        self.line = 0
        self.column = 0
        self.errorMessage = None

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

    def consumeWhitespace(self):
        """

        """

        while ( self.currChar == ' '
                or self.currChar == '\n'
                or self.currChar == '\r'
                or self.currChar == '\t' ):

            if self.currChar == '\n':
                self.line += 1
                self.column = 0

            if self.currChar == '\0':
                return

            self.charAdvance()

    # ------------------------------------------------------------------------------------------- #

    def consumeKeyword(self):
        """

        """

        length = 4 if (self.currChar == 't' or self.currChar == 'n') else 5

        for i in range(length):
            if self.currChar == '\0':
                self.errorMessage = "Incomplete JSON"
                return True
            self.charAdvance()

    # ------------------------------------------------------------------------------------------- #

    def consumeInt(self):
        """

        """

        while self.currChar.isdigit():
            if self.currChar == '\0':
                self.errorMessage = "Number never closed"
                return True

    # ------------------------------------------------------------------------------------------- #

    def consumeNumber(self):
        """

        """

        if self.currChar == '-':
            self.charAdvance()

            if not self.currChar.isdigit():
                self.errorMessage = "Invalid number"
                return True
            else:
                self.consumeInt()

        self.consumeInt()

        if self.currChar == 'e' or self.currChar == 'E':
            if self.currChar != '+' or self.currChar != '-':
                self.errorMessage = "Invalid number"
                return True
            else:
                self.charAdvance()

            if not self.currChar.isdigit():
                self.errorMessage = "Invalid number"
                return True
            else:
                self.consumeInt()

    # ------------------------------------------------------------------------------------------- #

    def consumeString(self):
        """

        """

        self.charAdvance()

        while True:
            if self.currChar == '\0':
                self.errorMessage = "String never closed"
                return True
            if self.currChar != '"':
                self.charAdvance()
            else:
                return

    # ------------------------------------------------------------------------------------------- #

    def consumeValue(self):
        """

        """

        self.consumeWhitespace()

        if self.currChar == '"':
            if self.consumeString(): return True
        elif self.currChar == '{':
            if self.consumeObject(): return True
        elif self.currChar == '[':
            if self.consumeArray(): return True
        elif self.currChar == 't' or self.currChar == 'n' or self.currChar == 'f':
            if self.consumeKeyword(): return True
        else:
            if self.consumeNumber(): return True

        self.consumeWhitespace()

    # ------------------------------------------------------------------------------------------- #

    def consumeObject(self):
        """

        """

        self.charAdvance()
        self.consumeWhitespace()

        if self.currChar == '}':
            self.charAdvance()
            return

        while True:
            if self.consumeString(): return True
            self.consumeWhitespace()

            if self.currChar == ':':
                self.charAdvance()
            else:
                self.errorMessage = "Invalid object"
                return True

            self.consumeWhitespace()
            if self.consumeValue(): return True

            if self.currChar == ',':
                self.charAdvance()
                self.consumeWhitespace()
            elif self.currChar == '}':
                self.charAdvance()
                self.consumeWhitespace()
                return
            else:
                self.errorMessage = "Invalid object"
                return True



    # ------------------------------------------------------------------------------------------- #

    def consumeArray(self):
        """

        """

        self.charAdvance()
        self.consumeWhitespace()
        while True:
            if self.consumeValue(): return True
            if self.currChar == ',':
                self.charAdvance()
                self.consumeWhitespace()
            else:
                break

        if self.currChar == ']':
            self.charAdvance()
            return
        else:
            self.errorMessage = "Array never closed"  # COULD BE BROKEN AS ITS NOT CURRENTLY WORKING GREAT IN C VERSION
            return True



    # ------------------------------------------------------------------------------------------- #

    @staticmethod
    def validateFileNames(fileNames):
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

        fileContent = ''

        with open(fileName, 'r') as file:
            line = file.readline()

            while line:
                fileContent += line
                line = file.readline()

        # print(sys.getsizeof(file_content))

        self.currContents = fileContent + '\0'
        self.pos, self.column, self.line = 0, 0, 0
        self.currChar = self.currContents[self.pos]

        self.consumeWhitespace()

        valid = True
        if self.currChar == '{':
            if self.consumeObject(): valid = False
        elif self.currChar == '[':
            if self.consumeArray(): valid = False

        self.consumeWhitespace()

        if not valid:
            print(self.errorMessage, " at line ", self.line, ", column ", self.column) # obviously needs to be converted to UI display later
        return valid

    # ------------------------------------------------------------------------------------------- #

    def validateFiles(self, fileNames, dirPath):
        """
        include handing for return
        """

        validFiles = []

        for file in fileNames:
            if system() == "Windows":
                if self.validateFile(dirPath + "\\\\" + file):
                    validFiles.append(file)
            else:
                if self.validateFile(dirPath + "/" + file):
                    validFiles.append(file)

        return validFiles

    # ------------------------------------------------------------------------------------------- #


# FOR TESTING ONLY
def main():
    v = JsonValidator("testFiles")

if __name__ == "__main__":
    main()