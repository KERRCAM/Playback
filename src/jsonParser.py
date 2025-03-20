# LIBRARY IMPORTS
import json
import time
from platform import system

# LOCAL IMPORTS
from jsonValidator import JsonValidator
from stream import Stream

# ----------------------------------------------------------------------------------------------- #

class JsonParser:
    """
    Takes valid JSON files and parses them in a workable python object for analysis.

    Loops over each valid file and makes a python object out of each JSON object in the file.
    Python object only retains the relevant information that we need.

    Finally resulting in a list of stream objects, containing the data from all the files.
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

    # ------------------------------------------------------------------------------------------- #

    # ------------------------------------------------------------------------------------------- #

    def parseFile(self, fileName):

        fileContent = ""

        with open(fileName, 'r') as file:
            line = file.readline()

            while line:
                fileContent += line
                line = file.readline()

        self.currContents = fileContent
        self.pos = 0
        self.currChar = self.currContents[self.pos]

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