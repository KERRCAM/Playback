# LIBRARY IMPORTS
import customtkinter as ctk
from zipfile import ZipFile 
from tkinter import filedialog, messagebox
import os

# LOCAL IMPORTS
from jsonParser import JsonParser
from jsonProcessor import JsonProcessor
from jsonValidator import JsonValidator
from mainMenu import *

# ----------------------------------------------------------------------------------------------- #

class UploadMenu:
    """
    This class is used for managing user uploaded spotify JSON files and has a segue to Main Menu.
    """

# ----------------------------------------------------------------------------------------------- #

    def __init__(self, window, mainWindow, username):
        self.username = username
        self.input_path = ""
        self.input_dir = ""

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
        frame = ctk.CTkFrame(uploadmenu, width=200, height=200, corner_radius=10, border_width=2)
        frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        label = ctk.CTkLabel(frame, text="Upload screen", font=("Helvetica", 20))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        mainMenuButton = ctk.CTkButton(frame, text="Drop files", font=("Helvetica", 20), command=self.UploadAction)
        mainMenuButton.grid(row=1, column=0, pady=10)

        # # Button to go to the main menu. May need to change the command to the main menu function
        temp_button = ctk.CTkButton(frame, text="Extract", font=("Helvetica", 20),
                                    command=self.main_menu_segue)
        temp_button.grid(row=1, column=1, pady=10)

        uploadmenu.protocol("WM_DELETE_WINDOW", lambda: self.close_window(uploadmenu))
        uploadmenu.mainloop()

    # ------------------------------------------------------------------------------------------- #

    # The function opens a folder to upload the file
    def UploadAction(self):
        try:
            self.input_path = filedialog.askopenfilename(filetypes=[('Zip file', '*.zip')])
            # Check if a file was selected
            if not self.input_path:
                messagebox.showerror("Error", "No file uploaded.")
                return
            else:
                # Get the directory of the uploaded file
                self.input_dir = os.path.dirname(self.input_path)
                extract_dir = os.path.join(self.input_dir, "extracted_files")

                # Call the extraction method with the directory of the uploaded file
                self.extraction(extract_dir)
                
        except Exception as e:
            print(f"Error: {e}")   

    # ------------------------------------------------------------------------------------------- #

    def extraction(self, output_dir):
        try:
            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Extract files to the specified output directory
            with ZipFile(self.input_path, 'r') as zip_file:
                zip_file.extractall(output_dir)

            # Validate extracted files
            if not os.listdir(output_dir):
                raise ValueError("The zip file is empty or contains no valid files.")

            # Process the extracted files
            v = JsonValidator(output_dir)
            print(output_dir)
            p = JsonParser(v.validFiles, v.dirPath)
            processor = JsonProcessor(p.streams, self.username) # NEED TO CHANGE TO CURRENT USERNAME

            messagebox.showinfo("Success", f"Files extracted to {output_dir}")
        except Exception as e:
            # Cleanup in case of failure
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    os.remove(os.path.join(output_dir, file))
                os.rmdir(output_dir)

            messagebox.showerror("Error", f"An error occurred during extraction: {e}")

    # ------------------------------------------------------------------------------------------- #

    def main_menu_segue(self):
        # Hides this window to show the next window
        self.window.withdraw()

        # Create the toplevel window
        signUp_window = ctk.CTkToplevel(self.window)

        # Initialise new window
        MainMenu(signUp_window, self.window, self.username)

    # ------------------------------------------------------------------------------------------- #

    def close_window(self, window):
        window.destroy()
        # Show the main window again
        self.loginMenu.deiconify()

# ----------------------------------------------------------------------------------------------- #

def main():
    root = ctk.CTk()
    app = UploadMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()