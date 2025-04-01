import json
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ulaaka_1223",
    database="playback"
)
cursor = conn.cursor()

def most_listened(cursor):
    """Top listened songs by the total minutes listened"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams
        FROM Songs
        ORDER BY timeListened DESC
        LIMIT 20
    """)
    return cursor.fetchall()

def most_streamed(cursor):
    """Most streamed songs"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams
        FROM Songs
        ORDER BY numberOfStreams DESC
        LIMIT 20
    """)
    return cursor.fetchall()

def most_played_artists(cursor):
    """Most Played Artists"""
    cursor.execute("""
        SELECT artist, numberOfStreams
        FROM Artists
        ORDER BY numberOfStreams DESC
        LIMIT 20
    """)
    return cursor.fetchall()

def most_skipped_songs(cursor):
    """Most Skipped Songs"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams, end_fwdbtn + end_backbtn AS total_skip
        FROM Songs
        ORDER BY total_skip DESC
        LIMIT 20
    """)
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


def plot_first_songs(cursor):
    songs = first_songs_year(cursor)
    names = [f"{row[1]}\n({row[2]})" for row in songs]
    dates = [row[3] for row in songs]

    for name, date in zip(names, dates):
        formatted_date = date.strftime('%Y/%m/%d')
        print(f"{formatted_date}: {name}")

plot_first_songs(cursor)

def plot_time_of_day(cursor):
    songs = time_of_day(cursor)
    morning = [{row[0]} for row in songs][0]
    afternoon = [{row[1]} for row in songs][0]
    evening = [{row[2]} for row in songs][0]
    night = [{row[3]} for row in songs][0]

    y = np.array([morning, afternoon, evening, night])
    mylabels = [f"Morning: {morning}", f"Afternoon: {afternoon}", f"Evening: {evening}", f"Night: {night}"]
    plt.pie(y, labels = mylabels)
    plt.show()

def plot_most_skipped_songs(cursor):
    songs = most_skipped_songs(cursor)
    names = [f"{row[0]}\n({row[1]})" for row in songs]
    times = [row[4] for row in songs]
    
    plt.figure(figsize=(15, 8))
    plt.barh(names, times, color='skyblue')
    plt.xlabel('Times Skipped')
    plt.title('Top Skipped Songs')
    plt.gca().invert_yaxis() 
    plt.tight_layout()
    plt.show()


def plot_top_songs_streaming(cursor):
    songs = most_streamed(cursor)
    names = [f"{row[0]}\n({row[1]})" for row in songs]
    times = [row[3] for row in songs]
    
    plt.figure(figsize=(15, 8))
    plt.barh(names, times, color='skyblue')
    plt.xlabel('Minutes streamed')
    plt.title('Top Songs by Streaming counts')
    plt.gca().invert_yaxis() 
    plt.tight_layout()
    plt.show()


def plot_most_played_artists(cursor):
    artists = most_played_artists(cursor)
    names = [f"{row[0]}" for row in artists]
    times = [row[1] for row in artists]
    
    plt.figure(figsize=(15, 8))
    plt.barh(names, times, color='skyblue')
    plt.xlabel('Times played')
    plt.title('Top artists')
    plt.gca().invert_yaxis() 
    plt.tight_layout()
    plt.show()