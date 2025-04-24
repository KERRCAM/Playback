"""
This class is used for managing user uploaded spotify JSON files and has a segue to Main Menu 

TO DO:
DROP BAR, ACCEPT BUTTON
file processing


IF HAVE TIME: 
DO LOADING SCREEN?

"""

# LIBRARY IMPORTS
import customtkinter as ctk

# LOCAL IMPORTS
from mainMenu import *
from jsonParser import *


class UploadMenu():

    def menuSegue(self):

        #self.jsonProcessor.


        # Hide the main window
        #self.root.withdraw()
        #
        # # Create the toplevel window
        # menu_window = ctk.CTkToplevel(self.root)
        #
        # mainMenu(menu_window, self.root)
        #
        # menu_window.title("Main Menu")
        # menu_window.geometry("800x600")
        #
        # # Handle the close button to return to login
        # menu_window.protocol("WM_DELETE_WINDOW", lambda: self.close_upload_window(menu_window))
        #
        return

    def close_window(self, window):
        window.destroy()
        # Show the main window again
        self.loginMenu.deiconify()

    def __init__(self, window, mainWindow):
        self.window = window
        uploadmenu = self.window
        self.loginMenu = mainWindow

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Create the main window
        uploadmenu.title("Playback")
        uploadmenu.geometry("800x600")
        # Allow resizing
        uploadmenu.resizable(width=True, height=True)

        # A frame to collect the labels and entry box
        frame = ctk.CTkFrame(
            uploadmenu,
            width=200,
            height=200,
            corner_radius=10,
            border_width=2
        )
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(frame, text="Upload screen", font=("Helvetica", 20))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        mainMenuButton = ctk.CTkButton(frame, text="Drop files", font=("Helvetica", 20))

        mainMenuButton.grid(row=1, column=0, pady=10)

        uploadmenu.protocol("WM_DELETE_WINDOW", lambda: self.close_window(uploadmenu))
        uploadmenu.mainloop()

def main():
    root = ctk.CTk()
    app = UploadMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()