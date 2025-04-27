import mysql.connector

class DB:
    def __init__(self):
        # password = input("Enter sql password: ")

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password= "Ulaaka_1223",
            database="playback"
        )

        self.cursor = self.db.cursor(buffered=True)