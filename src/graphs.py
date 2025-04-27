# LIBRARY IMPORTS

# LOCAL IMPORTS
import os
import matplotlib.pyplot as plt
import numpy as np
from queries import *
from db import DB


# ----------------------------------------------------------------------------------------------- #

class Graphs:
    """
    WHERE TO PUT SEARCH SORT ALGORITHMS

    Need to prioritise good run times and efficiency here as we are dealing with
    potentially tens of thousands of items needing sorted and hundreds of thousands
    needing to be searched through.

    So go more quick sorts, merge sorts and binary searches etc - best option in each case.
    Things like bubble sort and linear searches will be no good.

    ^ Can replace doc string once code is in, above is just a note.
    """

    @staticmethod
    def saveAsPng(fileName):
        script_dir = os.path.dirname("./src")
        results_dir = os.path.join(script_dir, 'Results/')

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        sample_file_name = f"{fileName}"
        plt.savefig(results_dir + sample_file_name)
        plt.close()

    def plot_total_listening_time_country(self):
        countries = self.queries.total_listening_time_country
        print(countries)
        country = [{row[0]} for row in countries]
        stats = [{row[2]} for row in countries]

        y = np.array([])
        for i in range(len(stats)):
            y = np.append(y, list(stats[i])[0])

        mylabels = []
        for i in range(len(country)):
            mylabels.append(f'{list(country[i])[0]}: {float("{:.2f}".format((y[i] / sum(y)) * 100))}%')

        plt.figure(facecolor='black')
        plt.pie(y, labels=mylabels, textprops={'color': 'white', 'fontweight': 'bold'})

        self.saveAsPng("totalListeningTimeCountry.png")
        plt.show()

    # The year (first year) that user started listening can be found by 0 as an argument
    def plot_top_artist_year(self, rankMax, yearNumber):
        artists_by_year = self.queries.top_artist_year
        print(artists_by_year)
        years = list(artists_by_year.keys())
        exactYear = years[yearNumber]
        names = [a[0] for a in artists_by_year[exactYear]]
        minutes = [a[1] / 3600 for a in artists_by_year[exactYear]]
        height = rankMax * 0.05
        plt.figure(figsize=(8, height))
        bar = plt.barh(names, minutes, color='green')
        plt.bar_label(
            bar,
            label_type='edge',
            color='white',
            fontweight='bold',
            padding=3
        )
        plt.xlabel('Total Minutes Played')
        plt.title(f'Top artists of {exactYear}')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("topArtistYear.png")

        plt.show()

    def plot_first_songs(self):
        # need to fix
        songs = self.queries.first_songs_year
        years = [row[2].year for row in songs]
        dates = [f"{row[2].year}:{row[2].month}:{row[2].day}" for row in songs]

        countries = [row[0] for row in songs]
        songNames = [row[1] for row in songs]

    def plot_time_of_day(self):
        songs = self.queries.time_of_day
        morning = [row[0] for row in songs][0]
        afternoon = [row[1] for row in songs][0]
        evening = [row[2] for row in songs][0]
        night = [row[3] for row in songs][0]

        y = np.array([morning, afternoon, evening, night])
        mylabels = [f'Morning: {float("{:.2f}".format((morning / sum(y)) * 100))}%',
                    f'Afternoon: {float("{:.2f}".format((afternoon / sum(y)) * 100))}%',
                    f'Evening: {float("{:.2f}".format((evening / sum(y)) * 100))}%',
                    f'Night: {float("{:.2f}".format((night / sum(y)) * 100))}%']
        plt.figure(facecolor='black')
        plt.pie(y, labels=mylabels, textprops={'color': 'white', 'fontweight': 'bold'})
        self.saveAsPng("timeOfDay.png")
        plt.show()

    def plot_most_skipped_songs(self, limit):
        songs = self.queries.most_skipped_songs
        names = [f"{row[0]} ({row[1]})" for row in songs]
        times = [row[4] for row in songs]
        height = limit * 0.4
        plt.figure(figsize=(8, height))
        plt.barh(names, times, color='green')
        plt.xlabel('Times Skipped')
        plt.title('Top Skipped Songs')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("mostSkippedSongs.png")

        plt.show()

    def plot_top_songs_streaming(self, limit):
        songs = self.queries.most_streamed
        names = [f"{row[0]} by {row[1]}" for row in songs]
        streams = [row[3] for row in songs]
        height = limit * 0.4
        plt.figure(figsize=(8, height))
        plt.barh(names, streams, color='green')
        plt.xlabel('Times streamed')
        plt.title('Top Streamed Songs')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("topSongsStreaming.png")

        plt.show()

    # not sure about this
    def plot_top_songs_listened(self, limit):
        songs = self.queries.most_listened
        names = [f"{row[0]} ({row[1]})" for row in songs]
        minutes = [row[2] / 60 for row in songs]
        height = limit * 0.4
        plt.figure(figsize=(8, height))
        plt.barh(names, minutes, color='green')
        plt.xlabel('Minutes listened')
        plt.title('Top Songs by Total Minutes Listened')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("topSongsListened.png")

        plt.show()

    def plot_most_played_artists(self, limit):
        artists = self.queries.most_played_artists
        names = [f"{row[0]}" for row in artists]
        times = [row[1] for row in artists]
        height = limit * 0.3
        plt.figure(figsize=(8, height))
        plt.barh(names, times, color='green')
        plt.xlabel('Times played')
        plt.title('Top artists')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("mostPlayedArtists.png")

        plt.show()

    def plot_most_common_end_reason(self):
        endReasons = self.queries.most_common_end_reason
        reasons = [row[0] for row in endReasons]
        counts = [row[1] for row in endReasons]
        y = np.array([counts[0], counts[1], counts[2], counts[3], counts[4]])
        mylabels = [f"{reasons[0]}: {counts[0]}", f"{reasons[1]}: {counts[1]}",
                    f"{reasons[2]}: {counts[2]}", f"{reasons[3]}: {counts[3]}",
                    f"{reasons[4]}: {counts[4]}"]
        plt.figure(facecolor='black', figsize=(8, 4))
        plt.pie(y, labels=mylabels, textprops={'color': 'white', 'fontweight': 'bold'})
        self.saveAsPng("mostCommonEndReason.png")
        plt.show()

    def __init__(self, username):
        self.username = username
        connection = DB()
        self.db = connection.db
        self.cursor = connection.cursor
        self.queries = Queries(self.username)

# ----------------------------------------------------------------------------------------------- #