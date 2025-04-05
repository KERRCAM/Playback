# LIBRARY IMPORTS
import time
import mysql.connector

# LOCAL IMPORTS
from jsonValidator import JsonValidator
from jsonParser import JsonParser
from datetime import datetime

# ----------------------------------------------------------------------------------------------- #

class JsonProcessor: # TODO - can remove all the db commits and just move one commit to the end of the loop for stream added

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

        sql = f"DELETE FROM Songs WHERE username = {self.username}"
        self.cursor.execute(sql)
        sql = f"DELETE FROM Albums WHERE username = {self.username}"
        self.cursor.execute(sql)
        sql = f"DELETE FROM Artists WHERE username = {self.username}"
        self.cursor.execute(sql)
        sql = f"DELETE FROM Episodes WHERE username = {self.username}"
        self.cursor.execute(sql)
        sql = f"DELETE FROM Shows WHERE username = {self.username}"
        self.cursor.execute(sql)
        sql = f"DELETE FROM Timestamps WHERE username = {self.username}"
        self.cursor.execute(sql)
        sql = f"DELETE FROM Countries WHERE username = {self.username}"
        self.cursor.execute(sql)
        sql = f"DELETE FROM Users WHERE username = {self.username}"
        self.cursor.execute(sql)

        self.db.commit()

    # ------------------------------------------------------------------------------------------- #

    def insertData(self):
        for i in self.streams:
            self.insertSong(i)
            self.insertAlbum(i)
            self.insertArtist(i)
            self.insertEpisode(i)
            self.insertShow(i)
            self.insertTimeStamp(i)
            self.insertCountry(i)
            self.insertUser(i)
        self.db.commit()

    # ------------------------------------------------------------------------------------------- #

    def insertSong(self, i):
        sql = f"SELECT songURI FROM Songs WHERE songURI = \"{i.spotify_track_uri}\""
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f"INSERT INTO Songs (songURI, username, songName, artist, album, timeListened, numberOfStreams, start_{i.reason_start}, end_{i.reason_end}) VALUES (\"{i.spotify_track_uri}\", \"{self.username}\", \"{i.master_metadata_track_name}\", \"{i.master_metadata_album_artist_name}\", \"{i.master_metadata_album_album_name}\", \"{i.ms_played}\", {1}, {1}, {1})"
            self.cursor.execute(sql)
        else:
            sql = f"SELECT timeListened, numberOfStreams, start_{i.reason_start}, end_{i.reason_end} FROM Songs WHERE songURI == \"{i.spotify_track_uri}\""
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            result[2] = 0 if result[2] is None else result[2]
            result[3] = 0 if result[3] is None else result[3]
            sql = f"UPDATE Songs SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1}, start_{i.reason_start} = {result[2] + 1}, end_{i.reason_end} = {result[3] + 1} WHERE songURI = \"{i.spotify_track_uri}\""
            self.cursor.execute(sql)

    # ------------------------------------------------------------------------------------------- #

    def insertAlbum(self, i):
        sql = f"SELECT album FROM Albums WHERE album = \"{i.master_metadata_album_album_name}\""
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f"INSERT INTO Albums (album, username, timeListened, numberOfStreams) VALUES (\"{i.master_metadata_album_album_name}\", \"{self.username}\", {i.ms_played}, {1})"
            self.cursor.execute(sql)
        else:
            sql = f"SELECT timeListened, numberOfStreams FROM Albums WHERE album = \"{i.master_metadata_album_album_name}\""
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            sql = f"UPDATE Albums SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1} WHERE album = \"{i.master_metadata_album_album_name}\""
            self.cursor.execute(sql)

    # ------------------------------------------------------------------------------------------- #

    def insertArtist(self, i):
        sql = f"SELECT artist FROM Artists WHERE artist = \"{i.master_metadata_album_artist_name}\""
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f"INSERT INTO Artists (artist, username, timeListened, numberOfStreams) VALUES (\"{i.master_metadata_album_artist_name}\", \"{self.username}\", {i.ms_played}, {1})"
            self.cursor.execute(sql)
        else:
            sql = f"SELECT timeListened, numberOfStreams FROM Artists WHERE artist = \"{i.master_metadata_album_artist_name}\""
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            sql = f"UPDATE Artists SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1} WHERE artist = \"{i.master_metadata_album_artist_name}\""
            self.cursor.execute(sql)

    # ------------------------------------------------------------------------------------------- #

    def insertEpisode(self, i):
        sql = f"SELECT episodeURI FROM Episodes WHERE episodeURI = \"{i.spotify_episode_uri}\""
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f"INSERT INTO Episodes (episodeURI, username, episodeName, showName, timeListened, numberOfStreams, start_{i.reason_start}, end_{i.reason_end}) VALUES (\"{i.spotify_episode_uri}\", \"{self.username}\", \"{i.episode_name}\", \"{i.episode_show_name}\", {i.ms_played}, {1}, {1}, {1})"
            self.cursor.execute(sql)
        else:
            sql = f"SELECT timeListened, numberOfStreams, start_{i.reason_start}, end_{i.reason_end} FROM Episodes WHERE episodeURI = \"{i.spotify_episode_uri}\""
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            sql = f"UPDATE Episodes SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1}, start_{i.reason_start} = {result[2] + 2}, end_{i.reason_end} = {result[3] + 1} WHERE episodeURI = \"{i.spotify_episode_uri}\""
            self.cursor.execute(sql)

    # ------------------------------------------------------------------------------------------- #

    def insertShow(self, i):
        sql = f"SELECT showName FROM Shows WHERE showName = \"{i.episode_show_name}\""
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f"INSERT INTO Shows (showName, username, timeListened, numberOfStreams) VALUES (\"{i.episode_show_name}\", \"{self.username}\", {i.ms_played}, {1})"
            self.cursor.execute(sql)
        else:
            sql = f"SELECT timeListened, numberOfStreams FROM Shows WHERE showName = \"{i.episode_show_name}\""
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            sql = f"UPDATE Shows Set timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1} WHERE showName = \"{i.episode_show_name}\""
            self.cursor.execute(sql)

    # ------------------------------------------------------------------------------------------- #

    def insertTimeStamp(self, i):
        sql = f"SELECT albumID FROM Albums WHERE album = \"{i.master_metadata_album_album_name}\""
        self.cursor.execute(sql)
        albumID = self.cursor.fetchone()
        sql = f"SELECT artistID FROM Artists WHERE artist = \"{i.master_metadata_album_artist_name}\""
        self.cursor.execute(sql)
        artistID = self.cursor.fetchone()
        dt = datetime.strptime(i.ts, "%Y-%m-%dT%H:%M:%SZ")
        ts = dt.strftime("%Y-%m-%d %H:%M:%S")
        sql = f"INSERT INTO Timestamps (username, songURI, episodeURI, albumID, artistID, timestamp) VALUES (\"{self.username}\", \"{i.spotify_track_uri}\", \"{i.spotify_episode_uri}\", {albumID[0]}, {artistID[0]}, \'{ts}\')"
        self.cursor.execute(sql)

    # ------------------------------------------------------------------------------------------- #

    def insertCountry(self, i):
        sql = f"SELECT albumID FROM Albums WHERE album = \"{i.master_metadata_album_album_name}\""
        self.cursor.execute(sql)
        albumID = self.cursor.fetchone()
        sql = f"SELECT artistID FROM Artists WHERE artist = \"{i.master_metadata_album_artist_name}\""
        self.cursor.execute(sql)
        artistID = self.cursor.fetchone()
        sql = f"SELECT showID FROM Shows WHERE showName = \"{i.episode_show_name}\""
        self.cursor.execute(sql)
        showID = self.cursor.fetchone()

        sql = f"SELECT numberOfStreams, timeListened FROM Countries WHERE countryCode = \"{i.conn_country}\""
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is None:
            sql = f"INSERT INTO Countries (username, songURI, episodeURI, albumID, artistID, showID, countryCode, numberOfStreams, timeListened) VALUES (\"{self.username}\", \"{i.spotify_track_uri}\", \"{i.spotify_episode_uri}\", {albumID[0]}, {artistID[0]}, {showID[0]}, \"{i.conn_country}\", {i.ms_played}, {1})"
            self.cursor.execute(sql)
        else:
            sql = f"UPDATE Countries SET numberOfStreams = {result[0] + 1}, timeListened = {result[1] + i.ms_played} WHERE countryCode = \"{i.conn_country}\""
            self.cursor.execute(sql)

    # ------------------------------------------------------------------------------------------- #

    def insertUser(self, i):
        dt = datetime.strptime(i.ts, "%Y-%m-%dT%H:%M:%SZ")
        ts = int(dt.strftime("%H"))

        timeOfDay = "night"
        if 6 < ts < 12:
            timeOfDay = "morning"
        elif 12 < ts < 18:
            timeOfDay = "afternoon"
        elif 18 < ts < 24:
            timeOfDay = "evening"

        sql = f"SELECT username FROM Users WHERE username = \"{self.username}\""
        self.cursor.execute(sql)
        if self.cursor.fetchone() is None:
            sql = f"INSERT INTO Users (username, timeListened, numberOfStreams, {timeOfDay}) VALUES (\"{self.username}\", {i.ms_played}, {1}, {1})"
            self.cursor.execute(sql)
        else:
            sql = f"SELECT timeListened, numberOfStreams, {timeOfDay} FROM Users WHERE username = \"{self.username}\""
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            sql = f"UPDATE Users SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1}, {timeOfDay} = {result[2] + 1} WHERE username = \"{self.username}\""
            self.cursor.execute(sql)

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