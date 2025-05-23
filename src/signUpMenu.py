# LIBRARY IMPORTS
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

# LOCAL IMPORTS
from dbconnection import DatabaseConnection
from db import *

# ----------------------------------------------------------------------------------------------- #

class SignUpMenu():
    """
    This class is used to accredit username and password at the first time.
    """

    # ----------------------------------------------------------------------------------------------- #

    def __init__(self, window, mainWindow):
        self.window = window
        signMenu = self.window
        # THIS IS USED FOR NAVIGATING BACK TO THE ORIGINAL WINDOW.
        self.loginMenu = mainWindow

        connection = DB()
        self.db = connection.db
        self.cursor = connection.cursor

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Create the main window
        signMenu.title("Playback")
        signMenu.geometry("800x600")

        # Allow resizing
        signMenu.resizable(width=True, height=True)

        # A frame to collect the labels and entry box
        frame = ctk.CTkFrame(signMenu, width=200, height=200, corner_radius=10, border_width=2)
        frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Title label
        label = ctk.CTkLabel(frame, text="Sign-Up screen", font=("Helvetica", 20))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username and password entry box and label
        usernameLabel = ctk.CTkLabel(frame, text="Username", font=("Helvetica", 20))
        usernameLabel.grid(row=1, column=0, padx=10, pady=10)

        passwordLabel = ctk.CTkLabel(frame, text="Password", font=("Helvetica", 20))
        passwordLabel.grid(row=2, column=0, padx=10, pady=10)

        # Username and password user input box - store as instance variables
        self.usernameInfo = ctk.CTkEntry(frame, font=("Helvetica", 20))
        self.usernameInfo.grid(row=1, column=1, padx=10, pady=10)

        # Show * for password
        self.passwordInfo = ctk.CTkEntry(frame, font=("Helvetica", 20), show="*")
        self.passwordInfo.grid(row=2, column=1, padx=10, pady=10)

        # Button to sign Up
        signUpButton = ctk.CTkButton(frame, text="Submit", command=self.getUserInfo)
        signUpButton.grid(row=3, column=1, padx=10, pady=20)

        signMenu.protocol("WM_DELETE_WINDOW", lambda: self.closeWindow(signMenu))
        signMenu.mainloop()

    # ------------------------------------------------------------------------------------------- #

    # On closing, this function will transition back to the main window
    def closeWindow(self, window):
        window.destroy()
        # Show the main window again
        self.loginMenu.deiconify()

    # ------------------------------------------------------------------------------------------- #

    # Gets username and password from the entry box
    def getUserInfo(self):
        username = self.usernameInfo.get()
        password = self.passwordInfo.get()

        print(f"Username and Password: {username} {password}")

        # This deletes datas in the entry box
        self.usernameInfo.delete(0, ctk.END)
        self.passwordInfo.delete(0, ctk.END)

        try:
            if self.signUpSuccessful(username, password):
                messagebox.showinfo("Success", "Account creation has been successfull")
                self.closeWindow(self.window)
            else:
                messagebox.showerror("Error", "Username already exists or an error occurred.")
        except Exception as e:
            messagebox.showerror("Error", e)
        return

    # ------------------------------------------------------------------------------------------- #

    def signUpSuccessful(self, username, password):
        try:
            # Check if username exists, then insert
            # Establish database connection

            # Check if the username already exists
            self.cursor.execute("""
                SELECT username
                FROM Users
                WHERE username = %s
            """, (username,))
            result = self.cursor.fetchone()

            if result:
                messagebox.showerror("Error", "This username already exists.")
                return False

                # Insert the new user into the database
            self.cursor.execute("""
                INSERT INTO Users (username, password)
                VALUES (%s, %s)
            """, (username, password))
            self.db.commit()

            print("Sign-up successful.")
            return True

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

# ----------------------------------------------------------------------------------------------- #
