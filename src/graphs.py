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
    Class for graph plotting.
    """

    # ------------------------------------------------------------------------------------------- #

    def __init__(self, username):

        self.username = username
        connection = DB()
        self.db = connection.db
        self.cursor = connection.cursor
        self.queries = Queries(self.username)

    # ------------------------------------------------------------------------------------------- #

    @staticmethod
    def saveAsPng(fileName):

        script_dir = os.path.dirname("./src")
        results_dir = os.path.join(script_dir, 'Results/')

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        sample_file_name = f"{fileName}"
        plt.savefig(results_dir + sample_file_name)
        plt.close()

    # ------------------------------------------------------------------------------------------- #

    def plot_total_listening_time_country(self):

        countries = self.queries.total_listening_time_country()
        country = [{row[0]} for row in countries]
        stats = [{row[2]} for row in countries]

        y = np.array([])
        for i in range(len(stats)):
            y = np.append(y, list(stats[i])[0])

        mylabels = []
        for i in range(len(country)):
            mylabels.append(f'{list(country[i])[0]}: {float("{:.2f}".format((y[i] / sum(y)) * 100))}%')
        grey = "#363636"
        plt.figure(facecolor=grey)
        plt.pie(y, labels=mylabels, textprops={'color': 'white', 'fontweight': 'bold'})

        self.saveAsPng("plot_total_listening_time_country.png")
        plt.show()

    # ------------------------------------------------------------------------------------------- #

    # The year (first year) that user started listening can be found by 0 as an argument
    def plot_top_artist_year(self, rankMax, yearNumber):

        artists_by_year = self.queries.top_artist_year()
        years = list(artists_by_year.keys())
        exactYear = years[yearNumber]
        names = [a[0] for a in artists_by_year[exactYear]]
        minutes = [a[1] / 3600 for a in artists_by_year[exactYear]]
        height = rankMax * 0.05
        grey = "#363636"
        plt.gca().set_facecolor(grey)
        plt.gca().figure.set_facecolor(grey)
        plt.gca().set_xlabel('Total Minutes Played', color="white")
        plt.gca().set_title(f'Top artists of {exactYear}', color="white")
        plt.gca().invert_yaxis()
        plt.tight_layout()

        plt.figure(figsize=(8, height))
        bar = plt.barh(names, minutes, color='green')
        plt.bar_label(
            bar,
            label_type='edge',
            color='white',
            fontweight='bold',
            padding=3
        )
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng(f"plot_top_artist_year_{exactYear}.png")
        plt.show()

    # ------------------------------------------------------------------------------------------- #

    def plot_first_songs(self):
        # need to fix
        songs = self.queries.first_songs_year()
        years = [row[2].year for row in songs]
        dates = [f"{row[2].year}:{row[2].month}:{row[2].day}" for row in songs]

        countries = [row[0] for row in songs]
        songNames = [row[1] for row in songs]

    # ------------------------------------------------------------------------------------------- #

    def plot_time_of_day(self):

        songs = self.queries.time_of_day()
        morning = [row[0] for row in songs][0]
        afternoon = [row[1] for row in songs][0]
        evening = [row[2] for row in songs][0]
        night = [row[3] for row in songs][0]

        y = np.array([morning, afternoon, evening, night])
        mylabels = [f'Morning: {float("{:.2f}".format((morning / sum(y)) * 100))}%',
                    f'Afternoon: {float("{:.2f}".format((afternoon / sum(y)) * 100))}%',
                    f'Evening: {float("{:.2f}".format((evening / sum(y)) * 100))}%',
                    f'Night: {float("{:.2f}".format((night / sum(y)) * 100))}%']
        grey = "#363636"
        plt.figure(facecolor=grey)
        plt.pie(y, labels=mylabels, textprops={'color': 'white', 'fontweight': 'bold'})
        self.saveAsPng("plot_time_of_day.png")
        plt.show()

    # ------------------------------------------------------------------------------------------- #

    def plot_most_skipped_songs(self, limit):

        songs = self.queries.most_skipped_songs(10)
        names = [f"{row[0]} ({row[1]})" for row in songs]
        times = [row[4] for row in songs]
        height = limit * 0.4
        grey = "#363636"
        plt.figure(figsize=(8, height))
        plt.barh(names, times, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().figure.set_facecolor(grey)
        plt.gca().set_xlabel('Times Skipped', color="white")
        plt.gca().set_title('Top Skipped Songs', color="white")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_most_skipped_songs.png")

        plt.show()

    # ------------------------------------------------------------------------------------------- #

    def plot_top_songs_streaming(self, limit):

        songs = self.queries.most_streamed(10)
        names = [f"{row[0]} by {row[1]}" for row in songs]
        streams = [row[3] for row in songs]
        height = limit * 0.4
        grey = "#363636"
        plt.figure(figsize=(8, height))
        plt.barh(names, streams, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().figure.set_facecolor(grey)
        plt.gca().set_xlabel('Times Streamed', color="white")
        plt.gca().set_title('Top Streamed Songs', color="white")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_top_songs_streaming.png")
        plt.show()

    # ------------------------------------------------------------------------------------------- #

    def plot_top_songs_listened(self, limit):

        songs = self.queries.most_listened(10)
        names = [f"{row[0]} ({row[1]})" for row in songs]
        minutes = [row[2] / 60 for row in songs]
        height = limit * 0.4
        grey = "#363636"
        plt.figure(figsize=(8, height))
        plt.barh(names, minutes, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().figure.set_facecolor(grey)
        plt.gca().set_xlabel('Minutes listened', color="white")
        plt.gca().set_title('Top Songs by Total Minutes Listened', color="white")
        plt.gca().tick_params(axis='x', colors="white")
        plt.gca().tick_params(axis='y', colors="white")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_top_songs_listened.png")
        plt.show()

    # ------------------------------------------------------------------------------------------- #

    def plot_most_played_artists(self, limit):

        artists = self.queries.most_played_artists(10)
        names = [f"{row[0]}" for row in artists]
        times = [row[1] for row in artists]
        height = limit * 0.3
        grey = "#363636"
        plt.figure(figsize=(8, height))
        plt.barh(names, times, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().figure.set_facecolor(grey)
        plt.gca().set_xlabel('Times played', color="white")
        plt.gca().set_title('Top artists', color="white")
        plt.gca().tick_params(axis='x', colors="white")
        plt.gca().tick_params(axis='y', colors="white")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_most_played_artists.png")
        plt.show()

    # ------------------------------------------------------------------------------------------- #

    def plot_most_played_episodes(self, limit):

        shows = self.queries.most_played_episodes_podcast(10)
        names = [f"{row[0]}" for row in shows]
        times = [row[1] for row in shows]
        height = limit * 0.3
        grey = "#363636"
        plt.figure(figsize=(8, height))
        plt.barh(names, times, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().set_xlabel('Times played', color="white")
        plt.gca().set_title('Top Episodes', color="white")
        plt.gca().tick_params(axis='x', colors="white")
        plt.gca().tick_params(axis='y', colors="white")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_most_played_episodes.png")
        plt.show()

    # ------------------------------------------------------------------------------------------- #

    def plot_most_common_end_reason(self):

        endReasons = self.queries.most_common_end_reason()
        reasons = [row[0] for row in endReasons]
        counts = [row[1] for row in endReasons]
        y = np.array([counts[0], counts[1], counts[2], counts[3], counts[4]])
        mylabels = [f"{reasons[0]}: {counts[0]}", f"{reasons[1]}: {counts[1]}",
                    f"{reasons[2]}: {counts[2]}", f"{reasons[3]}: {counts[3]}",
                    f"{reasons[4]}: {counts[4]}"]
        grey = "#363636"
        plt.figure(facecolor=grey, figsize=(8, 4))
        plt.pie(y, labels=mylabels, textprops={'color': 'white', 'fontweight': 'bold'})
        self.saveAsPng("plot_most_common_end_reason.png")
        plt.show()

# ----------------------------------------------------------------------------------------------- #
