# LIBRARY IMPORTS
import math
import time
import mysql.connector

# LOCAL IMPORTS
from jsonValidator import JsonValidator
from jsonParser import JsonParser

# ----------------------------------------------------------------------------------------------- #

class JsonProcessor():

# ----------------------------------------------------------------------------------------------- #

    def __init__(self):
        '''

        '''

        pswd = input("Enter sql password: ")

        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = pswd,
            database = "playback"
        )

        cursor = db.cursor()

        #sql = "INSERT INTO albums (album, username, timeListened, numberOfStreams) VALUES (%s, %s, %s, %s)"
        #val = ("Poetic Edda", "KC", 1230532, 354)
        #cursor.execute(sql, val)

        #db.commit()

        cursor.execute("SELECT * FROM albums")
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)

    # ------------------------------------------------------------------------------------------- #

# FOR TESTING ONLY
def main():
    start = time.time()
    v = JsonValidator("testFiles/testSet")
    p = JsonParser(v.validFiles, v.dirPath)
    print(len(p.streams))

    processor = JsonProcessor()

    end = time.time()
    print("Program run time = ", end - start, " seconds")

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------------------------- #