# LIBRARY IMPORTS
import os
import time
from os import listdir
from os.path import isfile, join
from platform import system
import re


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
    have written in C and is a public repository on my GitHub profile - Kerr Cameron.
    """


# ----------------------------------------------------------------------------------------------- #

    def __init__(self, folderName):
        """
        Constructor takes input of uploaded folder name.
        """

        fileNames, self.dirPath = self.getFiles(folderName)
        # validFileNames = self.validateFileNames(fileNames)
        self.validFiles = self.validateFiles(fileNames, self.dirPath)

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
            dirPath = os.path.relpath("..\\testFiles\\testSet", filePath) # hard coded path needs changed
        else:
            dirPath = os.path.relpath("../testFiles/testSet" ,filePath) # hard coded path needs changed
        fileNames = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]

        jsonFiles = []
        for file in fileNames:
            if file[-5:] == ".json":
                jsonFiles.append(file)

        return jsonFiles, dirPath

    # ------------------------------------------------------------------------------------------- #

    def charAdvance(self):
        """
        Moves curr char pointer to next char in input and increments current column.
        """

        self.pos += 1
        self.currChar = self.currContents[self.pos]
        self.column += 1

    # ------------------------------------------------------------------------------------------- #

    def consumeWhitespace(self):
        """
        Eats all leading whitespace from current point in file.
        Whitespace = (space* linefeed* carriageReturn* horizontalTab*)*

        :return: None if valid, True if error occurs
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
        Eats set JSON keywords
        Can be -> true | false | null

        :return: None if valid, True if error occurs
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
        Eats int all leading integer values.
        [0..9]*

        :return: None if valid, True if error occurs
        """

        while self.currChar.isdigit():
            if self.currChar == '\0':
                self.errorMessage = "Number never closed"
                return True
            else:
                self.charAdvance()

    # ------------------------------------------------------------------------------------------- #

    def consumeNumber(self):
        """
        Eats valid JSON number.
        Number = -? [1..9] [0..9]* (. [0..9]*)? (e or E - or + [0..9]*)

        :return: None if valid, True if error occurs
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
        Eats JSON string.
        startQuote (anyCharBut\* (\ any of -> quotes / \ b n f r t (u 4 hex digits)))  endQuote

        :return: None if valid, True if error occurs
        """

        self.charAdvance()

        while True:
            if self.currChar == '\0':
                self.errorMessage = "String never closed"
                return True
            if self.currChar == '\\':
                self.charAdvance()
                if self.currChar == '"':
                    self.charAdvance()
            if self.currChar != '"':
                self.charAdvance()
            else:
                self.charAdvance()
                return

    # ------------------------------------------------------------------------------------------- #

    def consumeValue(self):
        """
        Eats JSON value.
        Value = whitespace? object or array or string or number or bool or null whitespace?

        :return: None if valid, True if error occurs
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
        Eats JSON object.
        object = startCurly (whitespace)
        or (whitespace string whitespace? colon whitespace? value comma object*) endCurly

        :return: None if valid, True if error occurs
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
        Eats JSON array.
        Array = startSquare whitespace or (value comma)* endSquare

        :return: None if valid, True if error occurs
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
            self.errorMessage = "Array never closed"
            return True

    # ------------------------------------------------------------------------------------------- #

    @staticmethod
    def validateFileNames(fileNames):
        """
        Validates that the names of the input JSON files are as expected.
        Expected file name formats:
        "Streaming_History_Audio_YYYY.json"
        "Streaming_History_Audio_YYYY_X.json"
        "Streaming_History_Audio_YYYY-YYYY.json"
        "Streaming_History_Audio_YYYY-YYYY_X.json"

        :param fileNames: list of file names to validate
        :return: list of the valid file names
        """


        validFileNames = []

        # temporary - only checks for json files rn, will just use a regex later probably
        for file in reversed(fileNames):
            found = re.search("Streaming_History_Audio_[0-9]", file)
            if found is None or len(file) != len(found):
                fileNames.remove(file)

        return validFileNames

    # ------------------------------------------------------------------------------------------- #

    def validateFile(self, fileName):
        """
        Validates the input JSON file.

        :param fileName: JSON file name to be checked
        validJSON = whitespace? (array or object) whitespace? validJSON*
        """

        fileContent = ""

        with open(fileName, 'r') as file:
            line = file.readline()

            while line:
                fileContent += line
                line = file.readline()

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

        # Obviously needs to be converted to UI display later
        if not valid:
            print(self.currChar)
            print(fileName, ": ", self.errorMessage, " at line ", self.line, ", column ", self.column)
        else:
            print(fileName, "is valid JSON.")

        return valid

    # ------------------------------------------------------------------------------------------- #

    def validateFiles(self, fileNames, dirPath):
        """
        Calls correct validation on each of the input JSON files.

        :param fileNames : list of all input JSON files
        :param dirPath : directory path to the JSON files
        :return: list of the valid JSON files
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

# ----------------------------------------------------------------------------------------------- #

# FOR TESTING ONLY
def main():
    start = time.time()
    v = JsonValidator("testFiles/testSet")
    end = time.time()
    print("Program run time = ", end - start, " seconds")

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------------------------- #


