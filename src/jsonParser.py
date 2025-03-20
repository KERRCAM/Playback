# LIBRARY IMPORTS
import time

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

    def __init__(self, validFiles):
        """
        Constructor for the parser
        """


        self.streams = []

    # ------------------------------------------------------------------------------------------- #

# FOR TESTING ONLY
def main():
    start = time.time()
    v = JsonValidator("testFiles")
    p = JsonParser(v.validFiles)
    end = time.time()
    print("Program run time = ", end - start, " seconds")

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------------------------- #