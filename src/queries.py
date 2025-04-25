import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties


def connection_database():
    """Returns a new database connection"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ulaaka_1223",
        database="playback"
    )

def most_listened(cursor, limit):
    """Top listened songs by the total minutes listened"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams
        FROM Songs
        WHERE songName != 'null'
        ORDER BY timeListened DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def most_streamed(cursor, limit):
    """Most streamed songs"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams
        FROM Songs
        WHERE songName != 'null'
        ORDER BY numberOfStreams DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def most_played_artists(cursor, limit):
    """Most Played Artists"""
    cursor.execute("""
        SELECT artist, numberOfStreams
        FROM Artists
        WHERE artist != 'null'
        ORDER BY numberOfStreams DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def most_skipped_songs(cursor, limit):
    """Most Skipped Songs"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams, 
        COALESCE(end_fwdbtn, 0) + COALESCE(end_backbtn, 0) AS total_skip
        FROM Songs
        WHERE Songs.songName != 'null'
        ORDER BY total_skip DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def time_of_day(cursor):
    """Songs listened in each time of the day"""
    cursor.execute("""
        SELECT morning, afternoon, evening, night
        FROM Users
    """)
    return cursor.fetchall()
    

def first_songs_year(cursor):
    """Songs listened in each time of the day"""
    cursor.execute("""
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
    ORDER BY firstDate.year
    """)
    return cursor.fetchall()

def top_artist_year(cursor, resultsNumber):
    """Top artists in each year"""
    cursor.execute("""
        SELECT DISTINCT YEAR(timestamp) as year 
        FROM Timestamps 
        ORDER BY year DESC
    """)

    years = cursor.fetchall()
    total_years = [row[0] for row in years]

    year_dict = {}

    for i in total_years:
        cursor.execute("""
        SELECT A.artist, SUM(S.timeListened) AS total_time, COUNT(*) AS total_stream
        FROM Songs S
        JOIN Timestamps T ON S.songURI = T.songURI AND S.username = T.username
        JOIN Artists A ON S.artist = A.artist AND S.username = A.username
        WHERE YEAR(T.timestamp) = %s AND A.artist != 'null'
        GROUP BY A.artist
        ORDER BY total_time DESC
        LIMIT %s
        """, (i, resultsNumber))

        year_dict[i] = cursor.fetchall()

    return year_dict

def first_songs_year(cursor):
    """First songs listened in each country"""
    cursor.execute("""
    WITH RankedStreams AS (
        SELECT C.countryCode, T.songURI, T.timestamp,
        ROW_NUMBER() OVER (PARTITION BY C.countryCode ORDER BY T.timestamp) as ranking
        FROM Timestamps T
        JOIN Countries C ON C.songURI = T.songURI AND C.username = T.username
    )     
    SELECT countryCode, S.songName, timestamp
    FROM RankedStreams R
    JOIN Songs S ON R.songURI = S.songURI
    WHERE ranking <= 1
    ORDER BY countryCode, ranking

    """)
    return cursor.fetchall()

def total_listening_time_country(cursor):
    """Total streams listened in each country"""
    cursor.execute("""
        SELECT countryCode, count(numberOfStreams), sum(timeListened)
        FROM Countries
        GROUP BY countryCode
    """)
    return cursor.fetchall()

def most_common_end_reason(cursor):
    """Most common reason to end songs"""
    cursor.execute("""
        SELECT 'track finished' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_trackdone = 1
        UNION ALL
        SELECT 'used back button' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_backbtn = 1
        UNION ALL
        SELECT 'remote' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_remote = 1
        UNION ALL
        SELECT 'finished playing' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_endplay = 1
        UNION ALL
        SELECT 'skipped' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_fwdbtn = 1
        UNION ALL
        SELECT 'logout' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_logout = 1
        UNION ALL
        SELECT 'unexpected exit' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_unexpected_exit = 1
        UNION ALL
        SELECT 'unexpected exit while paused' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_unexpected_exit_while_paused = 1
        UNION ALL
        SELECT 'track error' AS ending_reasons, COUNT(*) AS count FROM Songs WHERE end_trackerror = 1  
        ORDER BY count DESC
    """)
    result = (cursor.fetchall())
    return result
