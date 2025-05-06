# LIBRARY IMPORTS
import customtkinter as ctk
import mysql.connector

# LOCAL IMPORTS
from uploadMenu import *
from signUpMenu import *
from mainMenu import *
from dbconnection import *  # This is the connection to the database

# ----------------------------------------------------------------------------------------------- #

class LoginMenu:
# ----------------------------------------------------------------------------------------------- #
   #firstTimeLogin = true  # This variable is used to check if the user has logged in before
    
    def __init__(self, root):
        self.root = root
        app = self.root

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Create the main window
        app.title("Playback")
        app.geometry("800x600")
        # Allow resizing
        app.resizable(width=True, height=True)
        
        # A frame to collect the labels and entry box
        frame = ctk.CTkFrame(app, width=200, height=200, corner_radius=10, border_width=2)
        frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Playback label
        PlaybackLabel = ctk.CTkLabel(app, text="Playback", font=("Helvetica", 30))
        PlaybackLabel.place(relx=0.50, rely=0.25, anchor=ctk.CENTER) 

        # App title
        label = ctk.CTkLabel(frame, text="Login to Your Account", font=("Helvetica", 20))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username and password label
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
        LoginButton = ctk.CTkButton(frame, text="Login", command=self.loginSegue)
        LoginButton.grid(row=3, column=0, padx=10, pady=20, columnspan=2)

        # Sign-up label
        SignUpLabel = ctk.CTkLabel(app, text="Don't have an account?", font=("Helvetica", 20))
        SignUpLabel.place(relx=0.37, rely=0.75, anchor=ctk.CENTER)  # Adjusted rely to place it below the frame

        # Sign-up button
        SignUpButton = ctk.CTkButton(app, text="Sign up", command=self.signUpSegue)
        SignUpButton.place(relx=0.6, rely=0.75, anchor=ctk.CENTER)  # Adjusted rely to place it below the label


    # ------------------------------------------------------------------------------------------- #

    # a method to verify username and password also create as well
    def user_authentication(self, username, password): 
        try:
            # activate db   
            #Establish database connection
            db = DatabaseConnection()                
            connection = db.connection_database()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT username, password
                FROM Users
                WHERE username = %s AND password = %s
            """, (username, password))
            result = cursor.fetchone()
            if result:
                print("Login successful")
                return True
            else:
                print("Login failed")
                return False
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # the button methods will do the transition to other screens and some stuffs
    def signUpSegue(self):
        username = self.usernameField.get()
        password = self.passwordField.get()

        print(f"{username} {password}")

        # Hide the main window
        self.root.withdraw()

        # Create the toplevel window
        signUp_window = ctk.CTkToplevel(self.root)
        # initialize UploadMenu
        SignUpMenu(signUp_window, self.root)
        return

    # ------------------------------------------------------------------------------------------- #

    def loginSegue(self,):
        username = self.usernameField.get()
        password = self.passwordField.get()

        print(f"Login attempt: {username} {password}")

        if self.user_authentication(username, password):            
            # Hide the main window
            self.root.withdraw()
            # Create the toplevelWindow
            login_window = ctk.CTkToplevel(self.root)
            # initialize UploadMenu
            UploadMenu(login_window, self.root, username)
            
        else:
            # Show an error message if authentication fails
            messagebox.showerror("Error", "Invalid username or password.")

# ----------------------------------------------------------------------------------------------- #

def main():
    root = ctk.CTk()
    app = LoginMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()