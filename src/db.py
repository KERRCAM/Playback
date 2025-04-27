# LIBRARY IMPORTS
import mysql.connector

# LOCAL IMPORTS


# ----------------------------------------------------------------------------------------------- #

class DB:
    """
    Class for setting a default database connection.
    """

# ----------------------------------------------------------------------------------------------- #

    def __init__(self):

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password= "seldomsmart456",
            database="playback"
        )

        self.cursor = self.db.cursor(buffered=True)

# ----------------------------------------------------------------------------------------------- #