# LIBRARY IMPORTS
import copy
import json
import time
from platform import system

# LOCAL IMPORTS
from jsonValidator import JsonValidator
from stream import Stream

# ----------------------------------------------------------------------------------------------- #

# TODO - NEED TO MAKE VALIDATOR UPDATE TO ONLY ACCEPT ARRAY -> OBJECTS

class JsonParser:
    """
    Takes valid JSON files and parses them in a workable python object for analysis.

    Loops over each valid file and makes a python object out of each JSON object in the file.
    Python object only retains the relevant information that we need.

    Finally resulting in a list of stream objects, containing the data from all the files.

    Parses ~19362 streams per file.
    """

# ----------------------------------------------------------------------------------------------- #

    def __init__(self, validFiles, dirPath):
        """
        Constructor for the parser
        """

        self.pos = 0
        self.currChar = None
        self.currContents = None

        self.streams = []

        self.streamTemplate = {
            "ts": None,
            "platform": None,
            "ms_played": None,
            "conn_country": None,
            "master_metadata_track_name": None,
            "master_metadata_album_artist_name": None,
            "master_metadata_album_album_name": None,
            "spotify_track_uri": None,
            "episode_name": None,
            "episode_show_name": None,
            "spotify_episode_uri": None,
            "reason_start": None,
            "reason_end": None,
        }

        self.currStream = None

        self.parseFiles(validFiles, dirPath)

    # ------------------------------------------------------------------------------------------- #

    def charAdvance(self):
        """
        Moves curr char pointer to next char in input.
        """

        self.pos += 1
        self.currChar = self.currContents[self.pos]

    # ------------------------------------------------------------------------------------------- #

    def skipWhitespace(self):
        """
        Skips all leading whitespace from current point in file.
        Whitespace = (space* linefeed* carriageReturn* horizontalTab*)*
        """

        while ( self.currChar == ' '
                or self.currChar == '\n'
                or self.currChar == '\r'
                or self.currChar == '\t' ):

            if self.currChar == '\0':
                return

            self.charAdvance()

    # ------------------------------------------------------------------------------------------- #

    def getNextString(self):

        string = ""

        self.charAdvance()
        while self.currChar != '"':
            if self.currChar == '\\':
                string += self.currChar
                self.charAdvance()
                string += self.currChar
                self.charAdvance()
            else:
                string += self.currChar
                self.charAdvance()

        return string

    # ------------------------------------------------------------------------------------------- #

    def getNextInt(self):

        number = 0
        while self.currChar.isdigit():
            number *= 10
            number += ord(self.currChar) - ord('0')
            self.charAdvance()

        return number

    # ------------------------------------------------------------------------------------------- #

    def getNextKeyword(self):

        keyword = ""
        while self.currChar != ',' and self.currChar != '}':
            keyword += self.currChar
            self.charAdvance()

        return keyword

    # ------------------------------------------------------------------------------------------- #

    def getNextValue(self):

        if self.currChar == '"':
            return self.getNextString()
        elif self.currChar.isdigit():
            return self.getNextInt()
        else:
            return self.getNextKeyword()

    # ------------------------------------------------------------------------------------------- #

    def parseStream(self):

        self.charAdvance()
        self.skipWhitespace()
        while self.currChar == '"':
            key = self.getNextString()
            self.charAdvance()
            self.charAdvance()
            self.charAdvance()

            value = self.getNextValue()

            self.charAdvance()
            if self.currChar == ',':
                self.charAdvance()
            self.skipWhitespace()

            # add key value pair to current stream dictionary
            if key in self.currStream:
                self.currStream[key] = value

    # ------------------------------------------------------------------------------------------- #

    def parseFile(self, fileName):

        fileContent = ""

        with open(fileName, 'r') as file:
            line = file.readline()

            while line:
                fileContent += line
                line = file.readline()

        self.currContents = fileContent + '\0'
        self.pos = 0
        self.currChar = self.currContents[self.pos]
        self.currStream = copy.deepcopy(self.streamTemplate)

        self.charAdvance()
        self.skipWhitespace()
        while self.currChar == '{':
            self.parseStream()
            newStream = Stream(self.currStream)
            self.streams.append(newStream)

    # ------------------------------------------------------------------------------------------- #

    def parseFiles(self, validFiles, dirPath):

        for file in validFiles:
            if system() == "Windows":
                file = dirPath + "\\\\" + file
            else:
                file = dirPath + "/" + file

            self.parseFile(file)

    # ------------------------------------------------------------------------------------------- #

# FOR TESTING ONLY
def main():
    start = time.time()
    v = JsonValidator("testFiles")
    p = JsonParser(v.validFiles, v.dirPath)
    end = time.time()
    print("Program run time = ", end - start, " seconds")

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------------------------- #
