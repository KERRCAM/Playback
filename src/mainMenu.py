"""
This is the main menu for the application.
It is also used to display the main menu of the application.


"""
# LIBRARY IMPORTS
import customtkinter as ctk
from tkinter import ttk
from queries import Queries

from PIL import Image

# LOCAL IMPORTS
from graphs import Graphs


class MainMenu:

    """
    BitmapImage for images in XBM format.
    PhotoImage for images in PGM, PPM, GIF and PNG formats. The latter is supported starting with Tk 8.6.
    """
    def imageProc(self):
        
        return

    def close_window(self, window):
        window.destroy()
        # Show the main window again
        self.prev_window.deiconify()

    def __init__(self, window, mainWindow):
        self.window = window
        mainMenu = self.window
        self.prev_window = mainWindow

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        mainMenu.title("Playback")
        mainMenu.geometry("1920x1080")
        mainMenu.resizable(width=True, height=True)

        q = Queries()
        print(q)
        q.first_songs_year_time()

        print(songData)
        table = ttk.Treeview(window, columns=('song', 'artist', 'streams', 'minuets'), show='headings')
        table.heading('song', text='Song')
        table.heading('artist', text='Artist')
        table.heading('streams', text='Streams')
        table.heading('minuets', text='Minuets')
        table.grid(padx = 50, pady = 100)
        table.place(x = 10, y = 50)

        j = 0
        for i in songData:
            table.insert('', j, values = (i['song'], i['artist'], i['streams'], i['minuets']))
            j += 1


        typeOption = ctk.CTkComboBox(mainMenu, values=["Song", "Album", "Artist", "Episode", "Show", "Country", "Time"], command=None)
        typeOption.grid(padx=5, pady=5)
        typeOption.set("Song")
        typeOption.place(x = 10, y = 5)

        # type.get() # gets option

        timeFrame = ctk.CTkComboBox(mainMenu, values=["2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017"], command=None)
        timeFrame.grid(padx=5, pady=5)
        timeFrame.set("2024")
        timeFrame.place(x = 180, y = 5)



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





def main():
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()