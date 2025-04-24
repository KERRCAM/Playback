"""
This class is used to accredit username and password at the first time

"""

# LIBRARY IMPORTS
import customtkinter as ctk
from tkinter import filedialog
from zipfile import ZipFile
from jsonValidator import JsonValidator
from jsonParser import JsonParser
from jsonProcessor import JsonProcessor
# from jsonProcessor import JsonProcessor
import time


# LOCAL IMPORTS

class UploadMenu():
    def __init__(self, window, main_window):
        self.window = window
        uploadmenu = self.window

        self.input_path = None

        uploadmenu.title("Playback")
        uploadmenu.geometry("800x600")
        uploadmenu.resizable(width=True, height=True)

        frame = ctk.CTkFrame(
            uploadmenu,
            width=200,
            height=200,
            corner_radius=10,
            border_width=2
        )
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(frame, text="Menu screen", font=("Helvetica", 20))
        label.pack(pady=10)  

        upload_button = ctk.CTkButton(
            frame,
            text="Upload",
            font=("Helvetica", 12),
            command=self.UploadAction
        )
        upload_button.pack(pady=10)

        extract_button = ctk.CTkButton(
            frame,
            text="Extract",
            font=("Helvetica", 12),
            command=self.extraction
        )
        extract_button.pack(pady=10)

        uploadmenu.mainloop()

    def callToPopulate(self):
        start = time.time()
        v = JsonValidator("testFiles/testSet")
        print("validated")
        p = JsonParser(v.validFiles, v.dirPath)
        print("parsed")
        print(p.streams)
        JsonProcessor(p.streams, "testUser")
        print("processed")
        end = time.time()
        print("Program run time = ", end - start, " seconds")

    # The snipped of code from the link below were used for the section down
    # https://stackoverflow.com/questions/70844511/i-want-to-upload-a-file-and-extract-it-using-python-tkinter-button-but-getting-e
    # acw1668
    def UploadAction(self):
        self.input_path = filedialog.askopenfilename(filetypes=[('Zip file', '*.zip')])
    

    def extraction(self):
        if self.input_path:
            with ZipFile(self.input_path, 'r') as zip_file:
                zip_file.extractall('/Users/nyamdorjbat-erdene/COMP208_G24/COMP208/testFiles/testSet')
        
        self.callToPopulate()