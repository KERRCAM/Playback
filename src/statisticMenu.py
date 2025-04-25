"""
This class will be used to show users graphs, charts and funny numbers kek

"""

# LIBRARY IMPORTS
import customtkinter as ctk
from tkinter import messagebox

# LOCAL IMPORTS


class statisticMenu:

    def close_window(self, window):
        window.destroy()
        # Show the main window again
        self.prev_window.deiconify()

    def __init__(self, root, prev_window):
        self.root = root
        stat_menu = self.root
        self.prev_window = prev_window
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # A frame to collect the labels and entry box
        frame = ctk.CTkFrame(stat_menu, width=200, height=200, corner_radius=10, border_width=2)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(frame, text="Upload screen", font=("Helvetica", 20))
        label.grid(row=0, column=0, columnspan=2, pady=10) 

        stat_menu.mainloop()