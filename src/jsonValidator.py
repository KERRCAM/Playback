# LIBRARY IMPORTS


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
    """

# -------------------------------------------------------------------------- #

    def __init__(self, folderName):
        """
        Constructor takes input of uploaded folder name
        """

        self.folderName = folderName

    # ---------------------------------------------------------------------- #

    def getFiles(self):
        """
        Gets all the JSON files names given in the uploaded folder
        :return: returns a list of the JSON files as strings
        """

        pass

    # ---------------------------------------------------------------------- #