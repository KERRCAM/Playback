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

        #self.most_common_end_reason = self.most_common_end_reason()

    # ------------------------------------------------------------------------------------------- #

    def most_listened(self, limit):
        """
        Top listened songs by the total minutes listened
        """

        self.cursor.execute("""
                    SELECT songName, artist, timeListened, numberOfStreams
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
                    SELECT songName, artist, timeListened, numberOfStreams
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

    def most_played_episodes_podcast(self, limit):
        """
        Most Played Shows
        """

        self.cursor.execute("""
                SELECT showName, numberOfStreams, timeListened
                FROM Episodes
                WHERE showName != 'null' and username = %s
                ORDER BY numberOfStreams DESC
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

    def first_songs_year_time(self):
        """
        Songs listened in each time of the day
        """

        self.cursor.execute("""
                    WITH firstDate AS (
                    SELECT
                        YEAR(timestamp) as year,
                        MIN(timestamp) as first
                    FROM Timestamps
                    GROUP BY YEAR(timestamp)
                )
                SELECT firstDate.year, Songs.songName, Songs.artist, firstDate.first as time_played 
                FROM firstDate    
                JOIN Timestamps ON firstDate.first = Timestamps.timestamp
                JOIN Songs ON Timestamps.songURI = Songs.songURI
                WHERE Songs.artist != 'null' and Songs.username = %s
                ORDER BY firstDate.year
                """, (self.username,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def top_artist_year(self, resultsNumber):
        """
        Top artists in each year
        """

        self.cursor.execute("""
                    SELECT DISTINCT YEAR(timestamp) as year 
                    FROM Timestamps 
                    WHERE artist != 'null' and username = %s
                    ORDER BY year DESC
                """, (self.username,))

        years = self.cursor.fetchall()
        total_years = [row[0] for row in years]
        year_dict = {}

        for i in total_years:
            self.cursor.execute("""
                    SELECT A.artist, SUM(S.timeListened) AS total_time, COUNT(*) AS total_stream
                    FROM Songs S 
                    JOIN Timestamps T ON S.songURI = T.songURI AND S.username = T.username
                    JOIN Artists A ON S.artist = A.artist AND S.username = A.username
                    WHERE YEAR(T.timestamp) = %s and S.artist != 'null' and S.username = %s
                    GROUP BY A.artist
                    ORDER BY total_time DESC
                    LIMIT %s
                    """, (i, self.username, resultsNumber,))
            year_dict[i] = self.cursor.fetchall()

        return year_dict

    # ------------------------------------------------------------------------------------------- #

    def first_songs_year_country(self):
        """
        First songs listened in each country
        """

        self.cursor.execute("""
                WITH RankedStreams AS (
                    SELECT C.countryCode, T.songURI, T.timestamp,
                    ROW_NUMBER() OVER (PARTITION BY C.countryCode ORDER BY T.timestamp) as ranking
                    FROM Timestamps T
                    JOIN Countries C ON C.songURI = T.songURI AND C.username = T.username
                )     
                SELECT countryCode, S.songName, timestamp
                FROM RankedStreams R
                JOIN Songs S ON R.songURI = S.songURI
                WHERE ranking <= 1 AND S.songName != 'null' AND C.username = %s
                ORDER BY countryCode, ranking
                """, (self.username, ))

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
        """, (self.username,))

        return self.cursor.fetchall()

    # ------------------------------------------------------------------------------------------- #

    def most_common_end_reason(self):
        """
        Most common reason to end songs
        """

        self.cursor.execute("""
                    SELECT 'track finished' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_trackdone = 1
                    UNION ALL
                    SELECT 'used back button' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_backbtn = 1
                    UNION ALL
                    SELECT 'remote' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_remote = 1
                    UNION ALL
                    SELECT 'finished playing' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_endplay = 1
                    UNION ALL
                    SELECT 'skipped' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_fwdbtn = 1
                    WHERE username = %s
                    ORDER BY count DESC
                """, (self.username, ))

        return self.cursor.fetchall()

# ----------------------------------------------------------------------------------------------- #