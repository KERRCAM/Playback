# LIBRARY IMPORTS
import math
import time
import mysql.connector

# LOCAL IMPORTS
from jsonValidator import JsonValidator
from jsonParser import JsonParser

# ----------------------------------------------------------------------------------------------- #

class JsonProcessor:

# ----------------------------------------------------------------------------------------------- #

    def __init__(self, streams, username):
        """
        Constructor for processor class.
        """

        password = input("Enter sql password: ")

        self.db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = password,
            database = "playback"
        )

        self.cursor = self.db.cursor()
        self.streams = streams
        self.username = username

        self.insertSongs()

    # ------------------------------------------------------------------------------------------- #

    def insertSongs(self):
        for i in self.streams:
            sql = f"SELECT songURI FROM songs WHERE songURI == {i.songURI}"
            self.cursor.execute(sql)
            if self.cursor.fetchone() is None:
                sql = f"INSERT INTO songs (songURI, username, songName, artist, album, timeListened, numberOfStreams, {i.reason_start}, {i.reason_end}) VALUES ({i.songURI}, {self.username}, {i.master_metadata_track_name}, {i.master_metadata_album_artist_name}, {i.master_metadata_album_album_name}, {i.ms_played}, {1}, {1}, {1})"
                self.cursor.execute(sql)
                self.db.commit()
            else:
                sql = f"SELECT timeListened, numberOfStreams, {i.reason_start}, {i.reason_end} FROM songs WHERE songURI == {i.songURI}"
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                result[2] = 0 if result[2] is None else result[2]
                result[3] = 0 if result[3] is None else result[3]
                sql = f"UPDATE songs SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1}, {i.reason_start} = {result[2] + 1}, {i.reason_end} = {result[3] + 1} WHERE songURI = {i.songURI}"
                self.cursor.execute(sql)
                self.db.commit()

    # ------------------------------------------------------------------------------------------- #

    def insertAlbums(self):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertArtists(self):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertEpisodes(self):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertShows(self):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertTimeStamps(self):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertCountries(self):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertUsers(self):
        pass

    # ------------------------------------------------------------------------------------------- #

# FOR TESTING ONLY
def main():
    start = time.time()
    v = JsonValidator("testFiles/testSet")
    p = JsonParser(v.validFiles, v.dirPath)
    print(len(p.streams))

    processor = JsonProcessor(p.streams, "testUser")

    end = time.time()
    print("Program run time = ", end - start, " seconds")

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------------------------- #