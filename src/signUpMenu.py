"""
This class is used to accredit username and password at the first time

"""

# LIBRARY IMPORTS
import customtkinter as ctk


# LOCAL IMPORTS
# mport mysql.connector

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

        usernameLabel = ctk.CTkLabel(frame, text="Username", font=("Helvetica", 20))
        usernameLabel.grid(row=1, column=0, padx=10, pady=10)

        passwordLabel = ctk.CTkLabel(frame, text="Password", font=("Helvetica", 20))
        passwordLabel.grid(row=2, column=0, padx=10, pady=10)

        # Username and password user input box - store as instance variables
        self.usernameField = ctk.CTkEntry(frame, font=("Helvetica", 20))
        self.usernameField.grid(row=1, column=1, padx=10, pady=10)

        self.passwordField = ctk.CTkEntry(frame, font=("Helvetica", 20), show="*")  # Show * for password
        self.passwordField.grid(row=2, column=1, padx=10, pady=10)

        # Buttons for login a sign-up - pass function references not calls
        submit = ctk.CTkButton(frame, text="Submit")
        submit.grid(row=3, column=0, padx=10, pady=20)

        usernameSignUp = self.usernameField.get()
        passwordSignUp = self.passwordField.get()
        
        """     conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Ulaaka_1223",
                database="playback"
            )
        cursor = conn.cursor()"""
        