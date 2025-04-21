"""



"""



# LIBRARY IMPORTS
import customtkinter as ctk

# LOCAL IMPORTS


class MainMenu():

    def __init__(self, window, mainWindow):
        self.window = window
        mainMenu = self.window
        #

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        mainMenu.title("Playback")
        mainMenu.geometry("800x600")
        # Allow resizing
        mainMenu.resizable(width=True, height=True)


        # A frame to collect the labels and entry box
        frame = ctk.CTkFrame(
            mainMenu,
            width=200,
            height=200,
            corner_radius=10,
            border_width=2
        )
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(frame, text="Main Menu", font=("Helvetica", 20))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        mainMenu.mainloop()

def main():
    root = ctk.CTk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()