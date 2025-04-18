# LIBRARY IMPORTS


# LOCAL IMPORTS
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from queries import *


# ----------------------------------------------------------------------------------------------- #

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

    conn = connection_database();
    cursor = conn.cursor()

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
        for year in artists_by_year:
            print(f"\n=== Top Artists of {year} ===")
            print(f"|{'Rank':<5}| {'Artist':<30}| {'Minutes':<10}| Streams|")
            position = 1
            for artist, minutes, streams in artists_by_year[year]:
                print(f"|Top {position:<5}| {artist:<30}| {minutes:<10.1f}| {streams}|")
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

    def plot_top_songs_streaming(cursor, limit):
        # failed attempt to use tkinter for plot
        root = tkinter.Tk()

        songs = most_streamed(cursor, limit)
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

    def plot_most_played_artists(cursor, limit):
        artists = most_played_artists(cursor, limit)
        names = [f"{row[0]}" for row in artists]
        times = [row[1] for row in artists]
        
        plt.figure(figsize=(15, 8))
        plt.barh(names, times, color='skyblue')
        plt.xlabel('Times played')
        plt.title('Top artists')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

# ----------------------------------------------------------------------------------------------- #


    # ------------------------------------------------------------------------------------------- #
