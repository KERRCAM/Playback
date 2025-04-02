import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ulaaka_1223",
    database="playback"
)
cursor = conn.cursor()

def most_listened(cursor, limit):
    """Top listened songs by the total minutes listened"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams
        FROM Songs
        ORDER BY timeListened DESC
        LIMIT %s
    """, (limit))
    return cursor.fetchall()

def most_streamed(cursor, limit):
    """Most streamed songs"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams
        FROM Songs
        ORDER BY numberOfStreams DESC
        LIMIT %s
    """, (limit))
    return cursor.fetchall()

def most_played_artists(cursor, limit):
    """Most Played Artists"""
    cursor.execute("""
        SELECT artist, numberOfStreams
        FROM Artists
        ORDER BY numberOfStreams DESC
        LIMIT %s
    """, (limit))
    return cursor.fetchall()

def most_skipped_songs(cursor, limit):
    """Most Skipped Songs"""
    cursor.execute("""
        SELECT songName, artist, timeListened, numberOfStreams, end_fwdbtn + end_backbtn AS total_skip
        FROM Songs
        ORDER BY total_skip DESC
        LIMIT %s
    """, (limit))
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
        WHERE YEAR(T.timestamp) = %s
        GROUP BY A.artist
        ORDER BY total_time DESC
        LIMIT %s
        """, (i, resultsNumber))

        year_dict[i] = cursor.fetchall()

    return year_dict

def first_songs_year(cursor, rank):
    """First songs listened listened in each country"""
    cursor.execute("""
    WITH RankedStreams AS (
        SELECT C.country, T.songURI, T.timestamp,
        ROW_NUMBER() OVER (PARTITION BY C.country ORDER BY T.timestamp) as ranking
        FROM Timestamps T
        JOIN Countries C ON C.songURI = T.songURI AND C.username = T.username
    )
    SELECT country, songURI, timestamp
    FROM RankedStreams
    WHERE ranking <= %s
    ORDER BY country, ranking

    """, (rank,))
    print(cursor.fetchall())
    return cursor.fetchall()

first_songs_year(cursor, 4)

def total_listening_time_country(cursor):
    """Total streams listened in each country"""
    cursor.execute("""
        SELECT country, streams
        FROM Countries
    """)
    return cursor.fetchall()


def plot_top_artist_year(cursor, rankMax):
    artists_by_year = top_artist_year(cursor, rankMax)
    for year in artists_by_year:
        print(f"\n=== Top Artists of {year} ===")
        print(f"{'Rank':<5} {'Artist':<30} {'Minutes':<10} Streams")
        position = 1
        for artist, minutes, streams in artists_by_year[year]:
            print(f"Top {position:<5} {artist:<30} {minutes:<10.1f} {streams}")
            position+=1

def plot_first_songs(cursor):
    songs = first_songs_year(cursor)
    names = [f"{row[1]}\n({row[2]})" for row in songs]
    dates = [row[3] for row in songs]

    for name, date in zip(names, dates):
        formatted_date = date.strftime('%Y/%m/%d')
        print(f"{formatted_date}: {name}")

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
    root = tkinter.Tk()

    songs = most_streamed(cursor)
    names = [f"{row[0]}\n({row[1]})" for row in songs]
    times = [row[3] for row in songs]
    
    fig = Figure(figsize=(15, 8), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(names, times)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

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