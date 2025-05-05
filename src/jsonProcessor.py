# LIBRARY IMPORTS
import copy
import time
import mysql.connector

# LOCAL IMPORTS
from jsonValidator import JsonValidator
from jsonParser import JsonParser
from datetime import datetime
from db import DB

# ----------------------------------------------------------------------------------------------- #

class JsonProcessor:

# ----------------------------------------------------------------------------------------------- #

    def __init__(self, streams, username):
        """
        Constructor for processor class.
        Contains all the dictionary defaults and database connection setup.
        """
                    
        """
        THE CONNECTION TO LINUX SERVER
        DELETE BEFORE FINAL PROJECT

        Host lxfarm01.csc.liv.ac.uk
        HostName lxfarm01.csc.liv.ac.uk 
        User psubattu

        Host lxfarm*.csc.liv.ac.uk
        User psubattu
        Macs hmac-sha2-512                        
        """

        connection = DB()
        self.db = connection.db
        self.cursor = connection.cursor

        self.streams = streams
        self.username = username

        self.songs = {}
        self.albums = {}
        self.artists = {}
        self.episodes = {}
        self.shows = {}
        self.countries = {}
        self.user = {   "timeListened": 0,
                        "numberOfStreams": 0,
                        "morning": 0,
                        "afternoon": 0,
                        "evening": 0,
                        "night": 0
                    }

        self.startEndBase = {
            "start_trackdone": 0,
            "start_fwdbtn": 0,
            "start_backbtn": 0,
            "start_remote": 0,
            "start_clickrow": 0,
            "start_trackerror": 0,
            "start_playbtn": 0,
            "start_appload": 0,
            "start_unknown": 0,
            "start_switched_to_audio": 0,
            "start_switched_to_video": 0,
            "end_trackdone": 0,
            "end_fwdbtn": 0,
            "end_backbtn": 0,
            "end_remote": 0,
            "end_endplay": 0,
            "end_logout": 0,
            "end_unexpected_exit": 0,
            "end_unexpected_exit_while_paused": 0,
            "end_trackerror": 0,
            "end_unknown": 0,
            "end_switched_to_audio": 0,
            "end_switched_to_video": 0
        }

        self.cleanData()
        self.insertData()

    # ------------------------------------------------------------------------------------------- #

    def cleanData(self):
        """
        Clears all data relating to a user -> ran before new insertion.
        """

        sql = f"DELETE FROM Songs WHERE username = %s"
        self.cursor.execute(sql, (self.username,))
        sql = f"DELETE FROM Albums WHERE username = %s"
        self.cursor.execute(sql, (self.username,))
        sql = f"DELETE FROM Artists WHERE username = %s"
        self.cursor.execute(sql, (self.username,))
        sql = f"DELETE FROM Episodes WHERE username = %s"
        self.cursor.execute(sql, (self.username,))
        sql = f"DELETE FROM Shows WHERE username = %s"
        self.cursor.execute(sql, (self.username,))
        sql = f"DELETE FROM Timestamps WHERE username = %s"
        self.cursor.execute(sql, (self.username,))
        sql = f"DELETE FROM Countries WHERE username = %s"
        self.cursor.execute(sql, (self.username,))
        sql = f"DELETE FROM Users WHERE username = %s"
        self.cursor.execute(sql, (self.username,))

        self.db.commit()

    # ------------------------------------------------------------------------------------------- #

    def insertData(self):
        """
        Loops through all the stream objects calling all the insert methods for each.
        Responsible for commiting the data after the inserts and updates are made.
        Also tracks rough progress for larger datasets.
        """

        n = 0
        for i in self.streams:
            n += 1
            if n % 10000 == 0:
                print(n)
            self.insertSong(i)
            self.insertAlbum(i)
            self.insertArtist(i)
            self.insertEpisode(i)
            self.insertShow(i)
            self.insertTimeStamp(i)
            self.insertCountry(i)
            self.insertUser(i)
        self.db.commit()

    print("Data processed")

    # ------------------------------------------------------------------------------------------- #

    def insertSong(self, i):
        """
        Inserts stream song data.
        :param i: current stream object.
        """

        sn = f"start_{i.reason_start}"
        en = f"end_{i.reason_end}"
        if i.spotify_track_uri in self.songs.keys():
            result = self.songs[i.spotify_track_uri]
            sr = result[2][sn] + 1
            er = result[2][en] + 1
            sql = f"UPDATE Songs SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1}, start_{i.reason_start} = {sr}, end_{i.reason_end} = {er} WHERE songURI = \"{i.spotify_track_uri}\""
            self.cursor.execute(sql)
            self.songs[i.spotify_track_uri][2][sn] += 1
            self.songs[i.spotify_track_uri][2][en] += 1
            self.songs[i.spotify_track_uri] = (result[0] + i.ms_played, result[1] + 1, self.songs[i.spotify_track_uri][2])
        else:
            sql = f"INSERT INTO Songs (songURI, username, songName, artist, album, timeListened, numberOfStreams, start_{i.reason_start}, end_{i.reason_end}) VALUES (\"{i.spotify_track_uri}\", \"{self.username}\", \"{i.master_metadata_track_name}\", \"{i.master_metadata_album_artist_name}\", \"{i.master_metadata_album_album_name}\", \"{i.ms_played}\", {1}, {1}, {1})"
            self.cursor.execute(sql)
            newStartEnd = copy.deepcopy(self.startEndBase)
            newStartEnd[sn] += 1
            newStartEnd[en] += 1
            self.songs[i.spotify_track_uri] = (i.ms_played, 1, newStartEnd)

    # ------------------------------------------------------------------------------------------- #

    def insertAlbum(self, i):
        """
        Inserts stream album data.
        :param i: current stream object.
        """

        if i.master_metadata_album_album_name in self.albums.keys():
            result = self.albums[i.master_metadata_album_album_name]
            sql = f"UPDATE Albums SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1} WHERE album = \"{i.master_metadata_album_album_name}\""
            self.cursor.execute(sql)
            self.albums[i.master_metadata_album_album_name] = (result[0] + i.ms_played, result[1] + 1)
        else:
            sql = f"INSERT INTO Albums (album, username, timeListened, numberOfStreams) VALUES (\"{i.master_metadata_album_album_name}\", \"{self.username}\", {i.ms_played}, {1})"
            self.cursor.execute(sql)
            self.albums[i.master_metadata_album_album_name] = (i.ms_played, 1)

    # ------------------------------------------------------------------------------------------- #

    def insertArtist(self, i):
        """
        Inserts stream artist data.
        :param i: current stream object.
        """

        if i.master_metadata_album_artist_name in self.artists.keys():
            result = self.artists[i.master_metadata_album_artist_name]
            sql = f"UPDATE Artists SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1} WHERE artist = \"{i.master_metadata_album_artist_name}\""
            self.cursor.execute(sql)
            self.artists[i.master_metadata_album_artist_name] = (result[0] + i.ms_played, result[1] + 1)
        else:
            sql = f"INSERT INTO Artists (artist, username, timeListened, numberOfStreams) VALUES (\"{i.master_metadata_album_artist_name}\", \"{self.username}\", {i.ms_played}, {1})"
            self.cursor.execute(sql)
            self.artists[i.master_metadata_album_artist_name] = (i.ms_played, 1)

    # ------------------------------------------------------------------------------------------- #

    def insertEpisode(self, i):
        """
        Inserts stream episode data.
        :param i: current stream object.
        """

        sn = f"start_{i.reason_start}"
        en = f"end_{i.reason_end}"
        if i.spotify_episode_uri in self.episodes.keys():
            result = self.episodes[i.spotify_episode_uri]
            sr = result[2][sn] + 1
            er = result[2][en] + 1
            sql = f"UPDATE Episodes SET timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1}, start_{i.reason_start} = {sr}, end_{i.reason_end} = {er} WHERE episodeURI = \"{i.spotify_episode_uri}\""
            self.cursor.execute(sql)
            self.episodes[i.spotify_episode_uri][2][sn] += 1
            self.episodes[i.spotify_episode_uri][2][en] += 1
            self.episodes[i.spotify_episode_uri] = (
            result[0] + i.ms_played, result[1] + 1, self.episodes[i.spotify_episode_uri][2])
        else:
            sql = f"INSERT INTO Episodes (episodeURI, username, episodeName, showName, timeListened, numberOfStreams, start_{i.reason_start}, end_{i.reason_end}) VALUES (\"{i.spotify_episode_uri}\", \"{self.username}\", \"{i.episode_name}\", \"{i.episode_show_name}\", {i.ms_played}, {1}, {1}, {1})"
            self.cursor.execute(sql)
            newStartEnd = copy.deepcopy(self.startEndBase)
            newStartEnd[sn] += 1
            newStartEnd[en] += 1
            self.episodes[i.spotify_episode_uri] = (i.ms_played, 1, newStartEnd)

    # ------------------------------------------------------------------------------------------- #

    def insertShow(self, i):
        """
        Inserts stream show data.
        :param i: current stream object.
        """

        if i.episode_show_name in self.shows.keys():
            result = self.shows[i.episode_show_name]
            sql = f"UPDATE Shows Set timeListened = {result[0] + i.ms_played}, numberOfStreams = {result[1] + 1} WHERE showName = \"{i.episode_show_name}\""
            self.cursor.execute(sql)
            self.shows[i.episode_show_name] = (result[0] + i.ms_played, result[1] + 1)
        else:
            sql = f"INSERT INTO Shows (showName, username, timeListened, numberOfStreams) VALUES (\"{i.episode_show_name}\", \"{self.username}\", {i.ms_played}, {1})"
            self.cursor.execute(sql)
            self.shows[i.episode_show_name] = (i.ms_played, 1)

    # ------------------------------------------------------------------------------------------- #

    def insertTimeStamp(self, i):
        """
        Inserts stream timestamp data.
        :param i: current stream object.
        """

        sql = f"INSERT INTO Timestamps (username, songURI, episodeURI, album, artist, timestamp) VALUES (\"{self.username}\", \"{i.spotify_track_uri}\", \"{i.spotify_episode_uri}\", \"{i.master_metadata_album_album_name}\", \"{i.master_metadata_album_artist_name}\", \'{i.ts}\')"
        self.cursor.execute(sql)

    # ------------------------------------------------------------------------------------------- #

    def insertCountry(self, i):
        """
        Inserts stream country data.
        :param i: current stream object.
        """

        if i.conn_country in self.countries.keys():
            result = self.countries[i.conn_country]
            sql = f"UPDATE Countries SET numberOfStreams = {result[0] + 1}, timeListened = {result[1] + i.ms_played} WHERE countryCode = \"{i.conn_country}\""
            self.cursor.execute(sql)
            self.countries[i.conn_country] = (result[0] + i.ms_played, result[1] + 1)
        else:
            sql = f"INSERT INTO Countries (username, songURI, episodeURI, album, artist, showName, countryCode, numberOfStreams, timeListened) VALUES (\"{self.username}\", \"{i.spotify_track_uri}\", \"{i.spotify_episode_uri}\", \"{i.master_metadata_album_album_name}\", \"{i.master_metadata_album_artist_name}\", \"{i.episode_show_name}\", \"{i.conn_country}\", {i.ms_played}, {1})"
            self.cursor.execute(sql)
            self.countries[i.conn_country] = (1, i.ms_played)

    # ------------------------------------------------------------------------------------------- #

    def insertUser(self, i):
        """
        Inserts a users overall data.
        :param i: the current stream object.
        """

        dt = datetime.strptime(i.ts, "%Y-%m-%d %H:%M:%S")
        ts = int(dt.strftime("%H"))

        timeOfDay = "night"
        if 6 < ts < 12:
            timeOfDay = "morning"
        elif 12 < ts < 18:
            timeOfDay = "afternoon"
        elif 18 < ts < 24:
            timeOfDay = "evening"

        if self.user["numberOfStreams"] != 0:
            sql = f"UPDATE Users SET timeListened = {self.user["timeListened"] + i.ms_played}, numberOfStreams = {self.user["numberOfStreams"] + 1}, {timeOfDay} = {self.user[timeOfDay] + 1} WHERE username = \"{self.username}\""
            self.cursor.execute(sql)
            self.user["timeListened"] += i.ms_played
            self.user["numberOfStreams"] += 1
            self.user[timeOfDay] += 1
        else:
            sql = f"INSERT INTO Users (username, timeListened, numberOfStreams, {timeOfDay}) VALUES (\"{self.username}\", {i.ms_played}, {1}, {1})"
            self.cursor.execute(sql)
            self.user["timeListened"] = i.ms_played
            self.user["numberOfStreams"] = 1
            self.user[f"{timeOfDay}"] = 1

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