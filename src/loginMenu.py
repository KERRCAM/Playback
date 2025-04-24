# LIBRARY IMPORTS
import customtkinter as ctk

# LOCAL IMPORTS
from uploadMenu import *
from signUpMenu import *

class LoginMenu:
    """
    BitmapImage for images in XBM format.
    PhotoImage for images in PGM, PPM, GIF and PNG formats. The latter is supported starting with Tk 8.6.
    """
    def imageProc(self):
        return

    # a method to verify username and password also create as well
    def dataSQL(self):
        # activate db
        return

    # the button methods will do the transition to other screens and some stuffs
    # Temporary method to switch between Pages
    def signUpSegue(self):
        username = self.usernameField.get()
        password = self.passwordField.get()

        print(f"{username} {password}")

        # Hide the main window
        self.root.withdraw()

        # Create the toplevel window
        signUp_window = ctk.CTkToplevel(self.root)

        # initialize SignUp menu
        SignUpMenu(signUp_window, self.root)

        signUp_window.title("Sign-up Menu")
        signUp_window.geometry("800x600")

        # Handle the close button to return to login screen
        signUp_window.protocol("WM_DELETE_WINDOW", lambda: self.close_upload_window(signUp_window))

        return

        # # THIS CREATES NEW WINDOW
        # signUpPage = ctk.CTk()
        # # AND CLOSES THE OLD ONE
        # self.root.destroy()
        #
        # #  initialize SignUpMenu
        # signup_app = SignUpMenu(signUpPage)
        # signUpPage.mainloop()
        # return

    def loginSegue(self):
        username = self.usernameField.get()
        password = self.passwordField.get()

        print(f"Login attempt: {username} {password}")

        # Hide the main window
        self.root.withdraw()

        # Create the toplevel window
        second_window = ctk.CTkToplevel(self.root)

        # initialize UploadMenu
        UploadMenu(second_window, self.root)

        second_window.title("Upload Menu")
        second_window.geometry("800x600")

        # Handle the close button to return to login
        second_window.protocol("WM_DELETE_WINDOW", lambda: self.close_upload_window(second_window))

        return

    def close_upload_window(self, window):
        window.destroy()
        self.root.deiconify()  # Show the main window again

    def __init__(self, root):
        self.root = root
        app = self.root

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create the main window
        app.title("Playback")
        app.geometry("800x600")
        # Allow resizing
        app.resizable(width=True, height=True)

        # A frame to collect the labels and entry box
        frame = ctk.CTkFrame(
            app,
            width=200,
            height=200,
            corner_radius=10,
            border_width=2
        )
        frame.pack(pady=40, padx=20, fill="both", expand=True)

        # App title
        label = ctk.CTkLabel(frame, text="Login screen", font=("Helvetica", 20))
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
        LoginButton.grid(row=3, column=0, padx=10, pady=20)

        SignUpButton = ctk.CTkButton(frame, text="Sign up", command=self.signUpSegue)
        SignUpButton.grid(row=3, column=1, padx=10, pady=20)


def main():
    root = ctk.CTk()
    app = LoginMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()