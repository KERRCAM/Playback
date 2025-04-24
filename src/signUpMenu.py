"""
This class is used to accredit username and password at the first time

"""

# LIBRARY IMPORTS
import customtkinter as ctk

# LOCAL IMPORTS

class SignUpMenu():
    def __init__(self, window, main_window):
        self.window = window
        self.main_window = main_window

        signMenu = self.window

        # Create the main window
        signMenu.title("Playback")
        signMenu.geometry("800x600")
        # Allow resizing
        signMenu.resizable(width=True, height=True)

        # A frame to collect the labels and entry box
        frame = ctk.CTkFrame(
            signMenu,
            width=200,
            height=200,
            corner_radius=10,
            border_width=2
        )
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(frame, text="Sign-Up screen", font=("Helvetica", 20))
        label.grid(row=0, column=0, columnspan=2, pady=10)
