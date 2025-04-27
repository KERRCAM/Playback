"""
This is the main menu for the application.
It is also used to display the main menu of the application.


"""
# LIBRARY IMPORTS
import customtkinter as ctk
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
        # Allow resizing
        mainMenu.resizable(width=True, height=True)

        # A frame to collect the labels and entry box
        # frame = ctk.CTkFrame(mainMenu, width=200, height=200, corner_radius=10, border_width=2)
        # frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        combobox = ctk.CTkComboBox(mainMenu, values=["Song", "Album", "Artist"], command=None)
        combobox.pack(padx=5, pady=5)
        combobox.set("Song")

        combobox.get() # gets option
        g = Graphs()
        g.plot_top_artist_year(100, 2)

        my_image = ctk.CTkImage(light_image=Image.open('results/topArtistYear.png'),
                                          dark_image=Image.open('results/topArtistYear.png'),
                                          size=(640, 400))  # Width x Height

        my_label = ctk.CTkLabel(mainMenu, text="", image=my_image, anchor="sw")
        my_label.pack(pady=10)

        mainMenu.mainloop()

def main():
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()