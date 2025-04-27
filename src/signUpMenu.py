"""
This class is used to accredit username and password at the first time

"""

# LIBRARY IMPORTS
import customtkinter as ctk
from tkinter import messagebox

# LOCAL IMPORTS

class SignUpMenu():
    # a method to verify username and password also create as well
    def dataSQL(self):
        # activate db
        return


    # On closing, this function will transition back to the main window
    def close_window(self, window):
        window.destroy()
        # Show the main window again
        self.loginMenu.deiconify()


    # Gets username and password from the entry box
    def get_user_info(self):
        username = self.usernameInfo.get()
        password = self.passwordInfo.get()

        print(f"Username and Password: {username} {password}")
        
        # This deletes datas in the entry box
        self.usernameInfo.delete(0, ctk.END)
        self.passwordInfo.delete(0, ctk.END)

        try:
            if self.sign_up_successful(username, password):
                messagebox.showinfo("Success", "Account creation has been successfull")
            else:
                messagebox.showerror("Error", "There is a error")
        except Exception as e:
            messagebox.showerror("Error", e)
        return
    
    
    def sign_up_successful(self, username, password):
        try:
            # Check if username exists, then insert


            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def __init__(self, window, mainWindow):
        self.window = window
        signMenu = self.window
        # THIS IS USED FOR NAVIGATING BACK TO THE ORIGINAL WINDOW.
        self.loginMenu = mainWindow

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

        self.passwordInfo = ctk.CTkEntry(frame, font=("Helvetica", 20), show="*")  # Show * for password
        self.passwordInfo.grid(row=2, column=1, padx=10, pady=10)

        # Button to sign Up
        signUpButton = ctk.CTkButton(frame, text="Submit", command=self.get_user_info)
        signUpButton.grid(row=3, column=1, padx=10, pady=20)

        signMenu.protocol("WM_DELETE_WINDOW", lambda: self.close_window(signMenu))
        signMenu.mainloop()

def main():
    root = ctk.CTk()
    app = SignUpMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()