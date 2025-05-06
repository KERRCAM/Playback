# LIBRARY IMPORTS
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# LOCAL IMPORTS
from dbconnection import *
from db import DB


# ----------------------------------------------------------------------------------------------- #

class Queries:

    # ----------------------------------------------------------------------------------------------- #

    def __init__(self, username):
        self.username = username
        connection = DB()
        self.db = connection.db
        self.cursor = connection.cursor

        # self.most_common_end_reason = self.most_common_end_reason()

    # ------------------------------------------------------------------------------------------- #

    def most_listened(self, limit):
        """
        Top listened songs by the total minutes listened
        """

        self.cursor.execute("""
                    SELECT songName, artist, timeListened, numberOfStreams, album
                    FROM Songs
                    WHERE artist != 'null' and username = %s
                    ORDER BY timeListened DESC
                    LIMIT %s
                """, (self.username, limit,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def most_streamed(self, limit):
        """
        Most streamed songs
        """

        self.cursor.execute("""
                    SELECT songName, artist, timeListened, numberOfStreams, album
                    FROM Songs
                    WHERE artist != 'null' and username = %s
                    ORDER BY numberOfStreams DESC
                    LIMIT %s
                """, (self.username, limit,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def most_played_artists(self, limit):
        """
        Most Played Artists
        """

        self.cursor.execute("""
                    SELECT artist, numberOfStreams, timeListened
                    FROM Artists
                    WHERE artist != 'null' and username = %s
                    ORDER BY numberOfStreams DESC
                    LIMIT %s
                """, (self.username, limit,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def most_played_podcast(self, limit):
        """
        Most Played Shows
        """

        self.cursor.execute("""
                SELECT showName, SUM(numberOfStreams) as numberOfStreams, SUM(timeListened) as timeListened
                FROM Episodes
                WHERE showName != 'null' and username = %s
                GROUP BY showName
                ORDER BY numberOfStreams DESC
                LIMIT %s
            """, (self.username, limit,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def most_played_episodes(self, limit):
        """
        Most Played Episodes
        """

        self.cursor.execute("""
                SELECT episodeName, numberOfStreams, timeListened, showName
                FROM Episodes
                WHERE episodeName != 'null' and username = %s
                ORDER BY timeListened DESC
                LIMIT %s
            """, (self.username, limit,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def most_skipped_songs(self, limit):
        """
        Most Skipped Songs
        """

        self.cursor.execute("""
                    SELECT songName, artist, timeListened, numberOfStreams, end_fwdbtn + end_backbtn AS total_skip
                    FROM Songs
                    WHERE artist != 'null' and username = %s
                    ORDER BY total_skip DESC
                    LIMIT %s
                """, (self.username, limit,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def time_of_day(self):
        """
        Songs listened in each time of the day
        """

        self.cursor.execute("""
            SELECT morning, afternoon, evening, night
            FROM Users
            WHERE username = %s
        """, (self.username,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def first_songs_year_time(self, yearInput, limit):
        """
        First songs of each year
        """
        self.cursor.execute("""
            SELECT MIN(timestamp)
            FROM Timestamps
            WHERE songURI != 'null' and username = %s and YEAR(timestamp) = %s
        """, (self.username, yearInput))

        result = self.cursor.fetchone()
        date = result[0].strftime('%Y-%m-%d')

        self.cursor.execute("""
            SELECT S.songName, S.artist, S.numberOfStreams, S.timeListened, S.album
            FROM Songs S
            JOIN Timestamps T ON T.songURI = S.songURI 
            WHERE S.artist!= 'null' and S.username = %s and DATE(T.timestamp) = %s
            ORDER BY S.timeListened
            LIMIT %s
        """, (self.username, date, limit))
        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def top_artist_year(self, yearInput, limit):
        """
        Top artists in given year (yearInput)
        """

        self.cursor.execute("""
        SELECT A.artist, SUM(S.timeListened), SUM(S.numberOfStreams)
        FROM Songs S 
        JOIN Timestamps T ON S.songURI = T.songURI AND S.username = T.username
        JOIN Artists A ON S.artist = A.artist AND S.username = A.username
        WHERE YEAR(T.timestamp) = %s and S.artist != 'null' and S.username = %s
        GROUP BY A.artist
        ORDER BY SUM(S.timeListened) DESC
        LIMIT %s
        """, (yearInput, self.username, limit,))
        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def top_albums(self, limit):
        """
        Top albums
        """
        self.cursor.execute("""
            SELECT album, timeListened, numberOfStreams
            FROM Albums
            WHERE album != 'null' and username = %s
            ORDER BY timeListened DESC
            LIMIT %s
        """, (self.username, limit))
        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def total_listening_time_country(self):
        """
        Total streams listened in each country
        """

        self.cursor.execute("""
            SELECT countryCode, count(numberOfStreams), sum(timeListened)
            FROM Countries
            WHERE username = %s
            GROUP BY countryCode
            ORDER BY numberOfStreams DESC
        """, (self.username,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def most_common_end_reason(self):
        """
        Most common reason to end songs
        """

        self.cursor.execute("""
                    SELECT 'track finished' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_trackdone <=1 AND username = %s
                    UNION ALL
                    SELECT 'used back button' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_backbtn <=1 AND username = %s
                    UNION ALL
                    SELECT 'remote' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_remote <=1 AND username = %s
                    UNION ALL
                    SELECT 'finished playing' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_endplay <=1 AND username = %s
                    UNION ALL
                    SELECT 'skipped' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_fwdbtn <= 1 AND username = %s
                    UNION ALL
                    SELECT 'skipped' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_logout <= 1 AND username = %s
                    UNION ALL
                    SELECT 'Unexpected or Unknown' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE (end_unexpected_exit_while_paused <= 1 OR  end_unexpected_exit <= 1 OR end_unknown <= 1)AND username = %s      
                    ORDER BY count DESC
                """, (
        self.username, self.username, self.username, self.username, self.username, self.username, self.username))
        return self.cursor.fetchall()

# ----------------------------------------------------------------------------------------------- #