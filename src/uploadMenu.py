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

class UploadMenu():
    def __init__(self, window):
        self.window = window
        uploadmenu = self.window

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

        uploadmenu.mainloop()

def main():
    root = ctk.CTk()
    app = UploadMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()