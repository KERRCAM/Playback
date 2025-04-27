import mysql.connector

class DB:
    def __init__(self):

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password= "seldomsmart456",
            database="playback"
        )

        self.cursor = self.db.cursor(buffered=True)