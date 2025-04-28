# LIBRARY IMPORTS
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

    def close_window(self, window):
        window.destroy()
        # Show the main window again
        self.prev_window.deiconify()

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

        g = Graphs(self.username)
        q = Queries(self.username)
        songData = q.most_streamed

        print(songData)
        table = ttk.Treeview(window, columns = ('rank', 'song', 'artist', 'minuets', 'streams'), show='headings', selectmode='browse', height = 45, )
        table.column('rank', width = 50, anchor = 'center')
        table.heading('rank', text = 'Rank')
        table.column('song', width = 300, anchor = 'w')
        table.heading('song', text = 'Song')
        table.column('artist', width = 250, anchor = 'w')
        table.heading('artist', text = 'Artist')
        table.column('minuets', width = 100, anchor = 'center')
        table.heading('minuets', text = 'Minuets')
        table.column('streams', width = 100, anchor = 'center')
        table.heading('streams', text = 'Streams')
        table.grid(padx = 5, pady = 5)
        table.place(x = 10, y = 37)

        for i in range(0, 100):
            current = songData[i]
            table.insert('', i, values = (i + 1, current[0], current[1], current[2], current[3]))


        self.typeOption = ctk.CTkComboBox(mainMenu, values=["Song", "Album", "Artist", "Episode", "Show", "Country", "Time"], command = self.checkStates)
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

        i1 = ctk.CTkImage(light_image=Image.open('results/topArtistYear.png'),
                                        dark_image=Image.open('results/topArtistYear.png'),
                                        size=(600, 280))  # Width x Height

        g1 = ctk.CTkLabel(mainMenu, text="", image=i1)
        g1.grid(padx=5, pady=5)
        g1.place(x = 820, y = 40)

        i2 = ctk.CTkImage(light_image=Image.open('results/mostPlayedArtists.png'),
                                dark_image=Image.open('results/mostPlayedArtists.png'),
                                size=(600, 280))  # Width x Height

        g2 = ctk.CTkLabel(mainMenu, text="", image=i2)
        g2.grid(padx=5, pady=5)
        g2.place(x=820, y=320)

        i3 = ctk.CTkImage(light_image=Image.open('results/timeOfDay.png'),
                                dark_image=Image.open('results/timeOfDay.png'),
                                size=(600, 280))  # Width x Height

        g3 = ctk.CTkLabel(mainMenu, text="", image=i3)
        g3.grid(padx=5, pady=5)
        g3.place(x=820, y=600)

        mainMenu.mainloop()

    # ------------------------------------------------------------------------------------------- #

    def checkStates(self, idk):
        q = Queries(self.username)
        to = self.typeOption.get()
        sb = self.sortBy.get()
        tf = self.timeFrame.get()

        if to == "Song" and sb == "Streams":
            data = q.most_streamed
            self.songTable(data)
        elif to == "Song" and sb == "Time listened":
            data = q.most_listened
            self.songTable(data)

    # ------------------------------------------------------------------------------------------- #

    def songTable(self, data):
        table = ttk.Treeview(self.window, columns=('rank', 'song', 'artist', 'minuets', 'streams'), show='headings',
                             selectmode='browse', height=45, )
        table.column('rank', width=50, anchor='center')
        table.heading('rank', text='Rank')
        table.column('song', width=300, anchor='w')
        table.heading('song', text='Song')
        table.column('artist', width=250, anchor='w')
        table.heading('artist', text='Artist')
        table.column('minuets', width=100, anchor='center')
        table.heading('minuets', text='Minuets')
        table.column('streams', width=100, anchor='center')
        table.heading('streams', text='Streams')
        table.grid(padx=5, pady=5)
        table.place(x=10, y=37)

        for i in range(0, 100):
            current = data[i]
            table.insert('', i, values=(i + 1, current[0], current[1], current[2], current[3]))

    # ------------------------------------------------------------------------------------------- #

    def graph1(self):
        pass

    # ------------------------------------------------------------------------------------------- #

    def graph2(self):
        pass

    # ------------------------------------------------------------------------------------------- #

    def graph3(self):
        pass

# ----------------------------------------------------------------------------------------------- #

def main():
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()