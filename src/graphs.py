# LIBRARY IMPORTS

# LOCAL IMPORTS
import os
import matplotlib.pyplot as plt
import numpy as np
from queries import *
from db import DB
import matplotlib.colors as mcolors
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

        result = self.queries.total_listening_time_country()
        countries = [row[0] for row in result]
        stats = [row[2] for row in result]


        colors = plt.cm.tab20.colors[:len(countries)]
        grey = "#363636"
        plt.title("Most Common End Reasons", color='white')

        plt.figure(facecolor=grey, figsize=(8, 4))

        wedges, autotexts = plt.pie(
            stats,
            colors=colors,
            textprops={'color': 'white'}
        )

        legend = plt.legend(
            wedges,
            [f"{reason}: {((count/sum(stats))*100):0.1f}% ({count})" for reason, count in zip(countries, stats)],
            title="Metrics",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            facecolor=grey,
            labelcolor='white'
        )
        legend.get_title().set_color('white')
        plt.tight_layout()
        self.saveAsPng("plot_total_listening_time_country.png")

    # ------------------------------------------------------------------------------------------- #

    # The year (first year) that user started listening can be found by 0 as an argument
    def plot_top_artist_year(self, yearNumber, limit):

        years = self.queries.top_artist_year(yearNumber, limit)
        names = [row[0] for row in years]
        minutes = [row[1] / 60 for row in years]
        height = limit * 0.5
        grey = "#363636"
        plt.figure(figsize=(8, height), facecolor=grey)
        plt.barh(names, minutes, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().set_xlabel('Minutes Listened', color = 'white')
        plt.gca().set_title(f"Top Artists listened in {yearNumber}", color = 'white')
        plt.gca().tick_params(axis='x', colors = 'white')
        plt.gca().tick_params(axis='y', colors= 'white')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng(f"plot_top_artist_year_{yearNumber}.png")

    # ------------------------------------------------------------------------------------------- #

    def plot_top_albums(self, limit):
        albums = self.queries.top_albums(limit)

        data = [(row[0], row[1]) for row in albums]
        data.sort(key=lambda x: x[1], reverse=False)

        names = [f"{row[0]}" for row in data]
        minutes = [f"{(row[1]/60):0.1f}" for row in data]

        height = limit * 0.4
        grey = "#363636"
        plt.figure(figsize=(12, height), facecolor=grey)
        plt.barh(names, minutes, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().set_xlabel('Minutes Listened', color = 'white')
        plt.gca().set_title('Top Albums listened', color = 'white')
        plt.gca().tick_params(axis='x', colors = 'white')
        plt.gca().tick_params(axis='y', colors= 'white')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_top_albums.png")


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

    # ------------------------------------------------------------------------------------------- #

    def plot_most_skipped_songs(self, limit):

        songs = self.queries.most_skipped_songs(10)
        names = [f"{row[0]} ({row[1]})" for row in songs]
        times = [row[4] for row in songs]
        height = limit * 0.6
        grey = "#363636"
        plt.figure(figsize=(8, height))
        plt.barh(names, times, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().figure.set_facecolor(grey)
        plt.gca().set_xlabel('Times Skipped', color="white")
        plt.gca().set_title('Top Skipped Songs', color="white")
        plt.gca().tick_params(axis='x', colors="white")
        plt.gca().tick_params(axis='y', colors="white")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_most_skipped_songs.png")

    # ------------------------------------------------------------------------------------------- #

    def plot_top_songs_streaming(self, limit):

        songs = self.queries.most_streamed(10)
        names = [f"{row[0]} by {row[1]}" for row in songs]
        streams = [row[3] for row in songs]
        height = limit * 0.6
        grey = "#363636"
        plt.figure(figsize=(8, height))
        plt.barh(names, streams, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().figure.set_facecolor(grey)
        plt.gca().set_xlabel('Times Streamed', color="white")
        plt.gca().set_title('Top Streamed Songs', color="white")
        plt.gca().tick_params(axis='x', colors="white")
        plt.gca().tick_params(axis='y', colors="white")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_top_songs_streaming.png")

    # ------------------------------------------------------------------------------------------- #

    def plot_top_songs_listened(self, limit):

        songs = self.queries.most_listened(10)
        names = [f"{row[0]} ({row[1]})" for row in songs]
        minutes = [row[2] / 60 for row in songs]
        height = limit * 0.6
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

    # ------------------------------------------------------------------------------------------- #

    def plot_most_played_artists(self, limit):

        artists = self.queries.most_played_artists(10)
        names = [f"{row[0]}" for row in artists]
        times = [row[1] for row in artists]
        height = limit * 0.6
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

    # ------------------------------------------------------------------------------------------- #

    def plot_most_played_podcasts(self, limit):

        shows = self.queries.most_played_podcast(10)
        names = [f"{row[0]}" for row in shows]
        times = [row[1] for row in shows]
        height = limit * 0.6
        grey = "#363636"
        plt.figure(figsize=(8, height), facecolor=grey)
        plt.barh(names, times, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().set_xlabel('Times played', color = 'white')
        plt.gca().set_title('Top Podcast Shows', color = 'white')
        plt.gca().tick_params(axis='x', colors = 'white')
        plt.gca().tick_params(axis='y', colors= 'white')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_most_played_podcasts.png")
    
    # ------------------------------------------------------------------------------------------- #

    def plot_most_played_episodes(self, limit):

        shows = self.queries.most_played_episodes(10)

        data = [(row[0], row[2]) for row in shows]
        data.sort(key=lambda x: x[1], reverse=False)

        names = [f"{row[0]}" for row in data]
        minutes = [f"{(row[1]/60):0.1f}" for row in data]

        height = limit * 0.6
        grey = "#363636"
        plt.figure(figsize=(12, height), facecolor=grey)
        plt.barh(names, minutes, color='green')
        plt.gca().set_facecolor(grey)
        plt.gca().set_xlabel('Minutes Listened', color = 'white')
        plt.gca().set_title('Top Podcast Episodes listened', color = 'white')
        plt.gca().tick_params(axis='x', colors = 'white')
        plt.gca().tick_params(axis='y', colors= 'white')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        self.saveAsPng("plot_most_played_episodes.png")

    # ------------------------------------------------------------------------------------------- #

    def plot_most_common_end_reason(self):

        endReasons = self.queries.most_common_end_reason()
        reasons = [row[0] for row in endReasons]
        counts = [row[1] for row in endReasons]

        colors = plt.cm.tab20.colors[:len(reasons)]
        grey = "#363636"
        plt.title("Most Common End Reasons", color='white')

        plt.figure(facecolor=grey, figsize=(8, 4))

        wedges, autotexts = plt.pie(
            counts,
            colors=colors,
            textprops={'color': 'white'}
        )

        legend = plt.legend(
            wedges,
            [f"{reason}: {((count/sum(counts))*100):0.1f}% ({count})" for reason, count in zip(reasons, counts)],
            title="Metrics",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            facecolor=grey,
            labelcolor='white'
        )
        legend.get_title().set_color('white')
        plt.tight_layout()
        self.saveAsPng("plot_most_common_end_reason.png")
# ----------------------------------------------------------------------------------------------- #
    # Type the year as 2025, 2024 etc.
    def plot_first_songs_year_time(self, year, limit):
        result = self.queries.first_songs_year_time(year, limit)
        songs = [f"{row[0]} by {row[1]} ({row[4]})" for row in result]
        height = len(songs) * 0.6 + 0.5
        grey = "#363636"
        plt.figure(figsize=(8, height), facecolor=grey)
        plt.yticks(
            range(len(songs)),
            songs,
            color='white',
            ha='left',
            va='center'
        )
        plt.gca().set_facecolor(grey)
        plt.title(f"First Songs listened in {year}", size=16, pad=20, color = 'white')

        plt.gca().xaxis.set_visible(False)
        plt.gca().yaxis.set_visible(True)
        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        plt.margins(y=0.05)
        plt.ylim(len(songs) - 0.5, -0.5)
        plt.gca().tick_params(axis='y', pad=15)
        plt.tight_layout(pad=2)
        self.saveAsPng(f"plot_first_songs_year_time_{year}.png")