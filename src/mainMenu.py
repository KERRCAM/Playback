# LIBRARY IMPORTS
import os
from os.path import isfile, join
from platform import system
import customtkinter as ctk
from tkinter import ttk
from queries import Queries
from PIL import Image

# LOCAL IMPORTS
from graphs import Graphs

# ----------------------------------------------------------------------------------------------- #

class MainMenu:
    """
    This is the main menu for the application.
    It is also used to display the main menu of the application.
    """

    # ------------------------------------------------------------------------------------------- #

    def __init__(self, window, mainWindow, username):
        self.username = username
        self.window = window
        mainMenu = self.window
        self.prev_window = mainWindow

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        mainMenu.title("Playback")
        mainMenu.geometry("1920x1080")
        mainMenu.resizable(width=True, height=True)

        self.typeOption = ctk.CTkComboBox(mainMenu, values=["Song", "Album", "Artist", "Episode", "Show", "Country"], command = self.checkStates)
        self.typeOption.grid(padx=5, pady=5)
        self.typeOption.set("Song")
        self.typeOption.place(x = 10, y = 5)

        self.sortBy = ctk.CTkComboBox(mainMenu, values=["Streams", "Time listened"], command = self.checkStates)
        self.sortBy.grid(padx=5, pady=5)
        self.sortBy.set("Streams")
        self.sortBy.place(x=180, y=5)

        self.timeFrame = ctk.CTkComboBox(mainMenu, values=["All", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017"], command = self.checkStates)
        self.timeFrame.grid(padx=5, pady=5)
        self.timeFrame.set("All")
        self.timeFrame.place(x = 350, y = 5)

        mainMenu.mainloop()

    # ------------------------------------------------------------------------------------------- #

    def close_window(self, window):
        window.destroy()
        # Show the main window again
        self.prev_window.deiconify()

    # ------------------------------------------------------------------------------------------- #

    def checkStates(self, holder):
        """
        Checks
        """

        q = Queries(self.username)
        g = Graphs(self.username)
        to = self.typeOption.get()
        sb = self.sortBy.get()
        tf = self.timeFrame.get()

        filePath = os.path.dirname(os.path.realpath(__file__))
        if system() == "Windows":
            dirPath = os.path.relpath("..\\src\\results", filePath)
        else:
            dirPath = os.path.relpath("../src/results", filePath)
        fileNames = [f for f in os.listdir(dirPath) if isfile(join(dirPath, f))]

        if to == "Song" and sb == "Streams":
            data = q.most_streamed(100)
            self.songTable(data)

            if not f"{self.username}_plot_top_songs_streaming.png" in fileNames:
                g.plot_top_songs_streaming(10)
            self.graph1(f"results/{self.username}_plot_top_songs_streaming.png")
            if not f"{self.username}_plot_most_common_end_reason.png" in fileNames:
                g.plot_most_common_end_reason()
            self.graph2(f"results/{self.username}_plot_most_common_end_reason.png")
            if not f"{self.username}_plot_first_songs_year_time_{int(self.timeFrame.get())}.png" in fileNames:
                g.plot_first_songs_year_time(10, int(self.timeFrame.get()))
            self.graph3(f"results/{self.username}_plot_first_songs_year_time_{int(self.timeFrame.get())}.png")

        elif to == "Song" and sb == "Time listened":
            data = q.most_listened(100)
            self.songTable(data)
            if not f"{self.username}_plot_top_songs_listened.png" in fileNames:
                g.plot_top_songs_listened(10)
            self.graph1(f"results/{self.username}_plot_top_songs_listened.png")
            if not f"{self.username}_plot_time_of_day.png" in fileNames:
                g.plot_time_of_day()
            self.graph2(f"results/{self.username}_plot_time_of_day.png")
            if not f"{self.username}_plot_most_skipped_songs.png" in fileNames:
                g.plot_most_skipped_songs(10)
            self.graph3(f"results/{self.username}_plot_most_skipped_songs.png")

        elif to == "Episode" and sb == "Time listened":
            data = q.most_played_episodes(100)
            self.podcastTable(data)
            if not f"{self.username}_plot_most_played_episodes.png" in fileNames:
                g.plot_most_played_episodes(10)
            self.graph1(f"results/{self.username}_plot_most_played_episodes.png")
            if not f"{self.username}_plot_most_played_podcasts.png" in fileNames:
                g.plot_most_played_podcasts(10)
            self.graph2(f"results/{self.username}_plot_most_played_podcasts.png")
            if not f"{self.username}_plot_most_played_artists.png" in fileNames:
                g.plot_most_played_artists(10)
            self.graph3(f"results/{self.username}_plot_most_played_artists.png")

        elif to == "Artist" and sb == "Time listened":
            data = q.most_played_artists(100)
            self.artistTable(data)
            if not f"{self.username}_plot_most_played_artists.png" in fileNames:
                g.plot_most_played_artists(10)
            self.graph1(f"results/{self.username}_plot_most_played_artists.png")
            if not f"{self.username}_plot_top_artist_year_{int(self.timeFrame.get())}.png" in fileNames:
                g.plot_top_artist_year(int(self.timeFrame.get()), 10)
            self.graph2(f"results/{self.username}_plot_top_artist_year_{int(self.timeFrame.get())}.png")
            if not f"{self.username}_plot_total_listening_time_country.png" in fileNames:
                g.plot_total_listening_time_country()
            self.graph3(f"results/{self.username}_plot_total_listening_time_country.png")

        elif to == "Album" and sb == "Time listened":
            data = q.top_albums(100)
            self.albumsTable(data)
            if not f"{self.username}_plot_top_albums.png" in fileNames:
                g.plot_top_albums(10)
            self.graph1(f"results/{self.username}_plot_top_albums.png")
            if not f"{self.username}_plot_top_artist_year_{int(self.timeFrame.get())}.png" in fileNames:
                g.plot_top_artist_year(int(self.timeFrame.get()), 10)
            self.graph2(f"results/{self.username}_plot_top_artist_year_{int(self.timeFrame.get())}.png")
            if not f"{self.username}_plot_first_songs_year_time_{int(self.timeFrame.get())}.png" in fileNames:
                g.plot_first_songs_year_time(int(self.timeFrame.get()), 10)
            self.graph3(f"results/{self.username}_plot_first_songs_year_time_{int(self.timeFrame.get())}.png")

        elif to == "Country" and sb == "Streams":
            data = q.total_listening_time_country()
            self.countryTable(data)
            if not f"{self.username}_plot_total_listening_time_country.png" in fileNames:
                g.plot_total_listening_time_country()
            self.graph1(f"results/{self.username}_plot_total_listening_time_country.png")
            if not f"{self.username}_plot_top_artist_year_{ int(self.timeFrame.get())}.png" in fileNames:
                g.plot_top_artist_year(int(self.timeFrame.get()), 10)
            self.graph2(f"results/{self.username}_plot_top_artist_year_{ int(self.timeFrame.get())}.png")
            if not f"{self.username}_plot_top_albums.png" in fileNames:
                g.plot_top_albums(10)
            self.graph3(f"results/{self.username}_plot_top_albums.png")

        elif to == "Show" and sb == "Time listened":
            data = q.most_played_podcast(100)
            self.podcastTable(data)
            if not f"{self.username}_plot_most_played_episodes.png" in fileNames:
                g.plot_most_played_episodes(10)
            self.graph2(f"results/{self.username}_plot_most_played_episodes.png")
            if not f"{self.username}_plot_most_played_podcasts.png" in fileNames:
                g.plot_most_played_podcasts(10)
            self.graph1(f"results/{self.username}_plot_most_played_podcasts.png")
            if not f"{self.username}_plot_most_played_artists.png" in fileNames:
                g.plot_most_played_artists(10)
            self.graph3(f"results/{self.username}_plot_most_played_artists.png")

    # ------------------------------------------------------------------------------------------- #

    def songTable(self, data):
        table = ttk.Treeview(self.window, columns=('rank', 'song', 'artist', 'seconds', 'streams'), show='headings',
                                selectmode='browse', height=45, )
        table.column('rank', width=50, anchor='center')
        table.heading('rank', text='Rank')
        table.column('song', width=300, anchor='w')
        table.heading('song', text='Song')
        table.column('artist', width=250, anchor='w')
        table.heading('artist', text='Artist')
        table.column('seconds', width=100, anchor='center')
        table.heading('seconds', text='Seconds')
        table.column('streams', width=100, anchor='center')
        table.heading('streams', text='Streams')
        table.grid(padx=5, pady=5)
        table.place(x=10, y=37)

        for i in range(0, len(data)):
            current = data[i]
            table.insert('', i, values=(i + 1, current[0], current[1], current[2], current[3]))

    # ------------------------------------------------------------------------------------------- #

    def podcastTable(self, data):

        table = ttk.Treeview(self.window, columns=('rank', 'show', 'seconds', 'streams'), show='headings',
                                selectmode='browse', height=45, )
        table.column('rank', width=50, anchor='center')
        table.heading('rank', text='Rank')
        table.column('show', width=400, anchor='w')
        table.heading('show', text='Show')
        table.column('seconds', width=175, anchor='center')
        table.heading('seconds', text='Seconds')
        table.column('streams', width=175, anchor='center')
        table.heading('streams', text='Streams')
        table.grid(padx=5, pady=5)
        table.place(x=10, y=37)

        for i in range(0, len(data)):
            current = data[i]
            table.insert('', i, values=(i + 1, current[0], current[2], current[1]))

    # ------------------------------------------------------------------------------------------- #

    def artistTable(self, data):

        table = ttk.Treeview(self.window, columns=('rank', 'artist', 'seconds', 'streams'), show='headings',
                                selectmode='browse', height=45, )
        table.column('rank', width=50, anchor='center')
        table.heading('rank', text='Rank')
        table.column('artist', width=400, anchor='w')
        table.heading('artist', text='Artist')
        table.column('seconds', width=175, anchor='center')
        table.heading('seconds', text='Seconds')
        table.column('streams', width=175, anchor='center')
        table.heading('streams', text='Streams')
        table.grid(padx=5, pady=5)
        table.place(x=10, y=37)

        for i in range(0, len(data)):
            current = data[i]
            table.insert('', i, values=(i + 1, current[0], current[2], current[1]))

    # ------------------------------------------------------------------------------------------- #

    def albumsTable(self, data):

        table = ttk.Treeview(self.window, columns=('rank', 'album', 'seconds', 'streams'), show='headings',
                                selectmode='browse', height=45, )
        table.column('rank', width=50, anchor='center')
        table.heading('rank', text='Rank')
        table.column('album', width=400, anchor='w')
        table.heading('album', text='Album')
        table.column('seconds', width=175, anchor='center')
        table.heading('seconds', text='Seconds')
        table.column('streams', width=175, anchor='center')
        table.heading('streams', text='Streams')
        table.grid(padx=5, pady=5)
        table.place(x=10, y=37)

        for i in range(0, len(data)):
            current = data[i]
            table.insert('', i, values=(i + 1, current[0], current[1], current[2]))

    # ------------------------------------------------------------------------------------------- #

    def countryTable(self, data):

        table = ttk.Treeview(self.window, columns=('rank', 'country', 'seconds', 'streams'), show='headings',
                                selectmode='browse', height=45, )
        table.column('rank', width=50, anchor='center')
        table.heading('rank', text='Rank')
        table.column('country', width=200, anchor='center')
        table.heading('country', text='Country')
        table.column('seconds', width=275, anchor='center')
        table.heading('seconds', text='Seconds')
        table.column('streams', width=275, anchor='center')
        table.heading('streams', text='Streams')
        table.grid(padx=5, pady=5)
        table.place(x=10, y=37)

        for i in range(0, len(data)):
            current = data[i]
            table.insert('', i, values=(i + 1, current[0], current[2], current[1]))

    # ------------------------------------------------------------------------------------------- #

    def graph1(self, fileName):

        i1 = ctk.CTkImage(light_image=Image.open(fileName),
                            dark_image=Image.open(fileName),
                            size=(600, 280))  # Width x Height

        g1 = ctk.CTkLabel(self.window, text="", image=i1)
        g1.grid(padx=5, pady=5)
        g1.place(x=820, y=40)

    # ------------------------------------------------------------------------------------------- #

    def graph2(self, fileName):

        i2 = ctk.CTkImage(light_image=Image.open(fileName),
                            dark_image=Image.open(fileName),
                            size=(600, 280))  # Width x Height

        g2 = ctk.CTkLabel(self.window, text="", image=i2)
        g2.grid(padx=5, pady=5)
        g2.place(x=820, y=320)

    # ------------------------------------------------------------------------------------------- #

    def graph3(self, fileName):

        i3 = ctk.CTkImage(light_image=Image.open(fileName),
                            dark_image=Image.open(fileName),
                            size=(600, 280))  # Width x Height

        g3 = ctk.CTkLabel(self.window, text="", image=i3)
        g3.grid(padx=5, pady=5)
        g3.place(x=820, y=600)

# ----------------------------------------------------------------------------------------------- #
