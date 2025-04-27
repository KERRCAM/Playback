# LIBRARY IMPORTS
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# LOCAL IMPORTS
from queries import *


# ----------------------------------------------------------------------------------------------- #
# heh
class CF():
    """
    WHERE TO PUT SEARCH SORT ALGORITHMS

    Need to prioritise good run times and efficiency here as we are dealing with
    potentially tens of thousands of items needing sorted and hundreds of thousands
    needing to be searched through.

    So go more quick sorts, merge sorts and binary searches etc - best option in each case.
    Things like bubble sort and linear searches will be no good.

    ^ Can replace doc string once code is in, above is just a note.
    """

    def plot_total_listening_time_country(cursor):
        countries = total_listening_time_country(cursor)
        country = [{row[0]} for row in countries]
        stats = [{row[2]} for row in countries]

        y = np.array([])
        for i in range(len(stats)):
            y = np.append(y, list(stats[i])[0])

        mylabels = []
        for i in range(len(country)):
            mylabels.append(list(country[i])[0])
        plt.pie(y, labels = mylabels)
        plt.show()

    def plot_top_artist_year(cursor, rankMax):
        artists_by_year = top_artist_year(cursor, rankMax)
        years = list(artists_by_year.keys())

        fig, axes = plt.subplots(nrows=len(years), figsize=(7, len(years) * 2))

        for ax, year in zip(axes, years):
            names = [a[0] for a in artists_by_year[year]]
            minutes = [float(a[1]) for a in artists_by_year[year]]

            ax.barh(names, minutes, color='green')
            ax.set_xlabel("Total Minutes Played")
            ax.set_title(f"Top Artists of {year}")
            ax.invert_yaxis()

        plt.tight_layout()
        plt.show()

    def plot_first_songs(cursor):
        # need to fix
        songs = first_songs_year(cursor)
        years = [row[2].year for row in songs]
        dates = [f"{row[2].year}:{row[2].month}:{row[2].day}" for row in songs]

        countries = [row[0] for row in songs]
        songNames = [row[1] for row in songs]
        
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

    def plot_top_songs_streaming(cursor, limit):
        songs = most_streamed(cursor, limit)
        names = [f"{row[0]}\nby {row[1]}" for row in songs]
        streams = [row[2] for row in songs]
        plt.figure(figsize=(10, 3))
        plt.barh(names, streams, color='skyblue')
        plt.xlabel('Times streamed')
        plt.title('Top Streamed Songs')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def plot_top_songs_listened(cursor, limit):
        songs = most_listened(cursor, limit)
        names = [f"{row[0]}\nby {row[1]}" for row in songs]
        minutes = [row[2] for row in songs]
        
        plt.figure(figsize=(10, 3))
        plt.barh(names, minutes, color='skyblue')
        plt.xlabel('Minutes listened')
        plt.title('Top Songs by Total Minutes Listened')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def plot_most_played_artists(cursor, limit):
        artists = most_played_artists(cursor, limit)
        names = [f"{row[0]}" for row in artists]
        times = [row[1] for row in artists]
        
        plt.figure(figsize=(10, 3))
        plt.barh(names, times, color='skyblue')
        plt.xlabel('Times played')
        plt.title('Top artists')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def plot_most_common_end_reason(cursor):
        endReasons = most_common_end_reason(cursor)
        reasons = [f"{row[0]}" for row in endReasons]
        counts = [row[1] for row in endReasons]

        y = np.array([counts[0], counts[1], counts[2], counts[3], counts[4]])
        mylabels = [f"{reasons[0]}: {counts[0]}", f"{reasons[1]}: {counts[1]}", f"{reasons[2]}: {counts[2]}", f"{reasons[3]}: {counts[3]}", f"{reasons[4]}: {counts[4]}"]
        plt.pie(y, labels = mylabels)
        plt.show()

    plot_most_common_end_reason(5)

    def ___init__(self):
        # Create an instance of DatabaseConnection
        db = DatabaseConnection()
        connection = db.connection_database()

        # Pass the connection to Queries
        queries = queries(connection.cursor())
        pass

# ----------------------------------------------------------------------------------------------- #


    # ------------------------------------------------------------------------------------------- #
