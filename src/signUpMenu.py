"""
This class is used to accredit username and password at the first time

"""

# LIBRARY IMPORTS
import customtkinter as ctk

# LOCAL IMPORTS

class SignUpMenu():
    def close_window(self, window):
        window.destroy()
        # Show the main window again
        self.loginMenu.deiconify()

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
        signMenu.protocol("WM_DELETE_WINDOW", lambda: self.close_window(signMenu))

        signMenu.mainloop()

def main():
    root = ctk.CTk()
    app = SignUpMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()