# LIBRARY IMPORTS
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

        self.insertData()

    # ------------------------------------------------------------------------------------------- #

    def cleanData(self):

        # delete all database entries under given username for class
        sql = f"DELETE FROM songs WHERE username = {self.username}"
        self.cursor.execute(sql)

        # do for all

        self.db.commit()

    # ------------------------------------------------------------------------------------------- #

    def insertData(self):
        for i in self.streams:
            self.insertSong(i)
            self.insertAlbum(i)
            self.insertArtist(i)
            self.insertEpisode(i)

    # ------------------------------------------------------------------------------------------- #

    def insertSong(self, i):
        sql = f"SELECT songURI FROM songs WHERE songURI = {i.songURI}"
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

    def insertAlbum(self, i):
        sql = f"SELECT album FROM albums WHERE album = {i.master_metadata_album_album_name}"
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f"INSERT INTO albums album, username, timeListened, numberOfStreams VALUES ({i.master_metadata_album_album_name}, {self.username}, {i.ms_played}, {1})"
            self.cursor.execute(sql)
            self.db.commit()
        else:
            sql = f"SELECT timeListened, numberOfStreams FROM albums WHERE album = {i.master_metadata_album_album_name}"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            sql = f"UPDATE albums SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1} WHERE album = {i.album}"
            self.cursor.execute(sql)
            self.db.commit()

    # ------------------------------------------------------------------------------------------- #

    def insertArtist(self, i):
        sql = f"SELECT artist FROM artists WHERE artist = {i.master_metadata_album_artist_name}"
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f"INSERT INTO artists artist, username, timeListened, numberOfStreams VALUES ({i.master_metadata_album_artist_name}, {self.username}, {i.ms_played}, {1})"
            self.cursor.execute(sql)
            self.db.commit()
        else:
            sql = f"SELECT timeListened, numberOfStreams FROM artists WHERE artist = {i.master_metadata_album_artist_name}"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            sql = f"UPDATE artists SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1} WHERE artists = {i.master_metadata_album_artist_name}"
            self.cursor.execute(sql)
            self.db.commit()

    # ------------------------------------------------------------------------------------------- #

    def insertEpisode(self, i):

        # episodeURI username episodeName showName timeListened numberOfStreams reasonStart reasonEnd countriesListened

        sql = f"SELECT episodeURI FROM episodes WHERE episodeURI = {i.episodeURI}"
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f""


    # ------------------------------------------------------------------------------------------- #

    def insertShow(self, i):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertTimeStamp(self, i):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertCountry(self, i):
        pass

    # ------------------------------------------------------------------------------------------- #

    def insertUser(self, i):
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