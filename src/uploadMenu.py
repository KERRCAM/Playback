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
from zipfile import ZipFile
from tkinter import filedialog

# LOCAL IMPORTS
from mainMenu import *
from jsonParser import *
from jsonProcessor import *


class UploadMenu():

    """
    The code snippet both UploadAction(), extraction() are in credit to acw1668
    https://stackoverflow.com/questions/70844511/i-want-to-upload-a-file-and-extract-it-using-python-tkinter-button-but-getting-eacw1668
    """

    # The function opens a folder to upload the file
    def UploadAction(self):
        try:
            self.input_path = filedialog.askopenfilename(filetypes=[('Zip file', '*.zip')])
            actionCompleteLabel = ctk.CTkLabel(self.frame, text="The file has been received.", font=("Helvetica", 20))
            actionCompleteLabel.grid(row=2, column=0, pady=10)
        except Exception as e:
            print(f"Error: {e}")   


    # The function will extract given file and Validate and Parse.
    def extraction(self):
        if self.input_path:
            with ZipFile(self.input_path, 'r') as zip_file:
                zip_file.extractall(r"C:\Users\Dell\Desktop\Playback\testFiles\testSet")
                start = time.time()
                v = JsonValidator("testFiles/testSet")
                p = JsonParser(v.validFiles, v.dirPath)

                processor = JsonProcessor(p.streams, "testUser")
                end = time.time()
                print("Program run time = ", end - start, " seconds")


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

        mainMenuButton = ctk.CTkButton(frame, text="Drop files", font=("Helvetica", 20), command=self.UploadAction)
        mainMenuButton.grid(row=1, column=0, pady=10)
        
        extract_button = ctk.CTkButton(
            frame,
            text="Extract",
            font=("Helvetica", 20),
            command=self.extraction
        )
        extract_button.grid(row=1, column=1, pady=10)

        uploadmenu.protocol("WM_DELETE_WINDOW", lambda: self.close_window(uploadmenu))
        uploadmenu.mainloop()

def main():
    root = ctk.CTk()
    app = UploadMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()