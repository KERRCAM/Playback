"""
This class is for Front UI more specifically, Login page, Main Menu, sending and getting files, 
Graphs, Pie charts, and a drop down menu to search more specific thingies and quirky stuffs.

Also an ability to show custom image, icons, and share files.
Three windows with pop up windows

Possible colour pallettes:

    Black   #090D09
    Dark green #284032
    Blue green #3B8C6E
    White   
    Grey  
"""

import customtkinter as ctk

class login():


    def loginPage():



        return
    

    def mainMenu():
        root = ctk()
        frm = ctk.Frame(root, padding=10)
        frm.grid()
        ctk.Label(frm, text="Hello World!").grid(column=0, row=0)
        ctk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
        root.mainloop()
        return
    
    """
    BitmapImage for images in XBM format.
    
    PhotoImage for images in PGM, PPM, GIF and PNG formats. The latter is supported starting with Tk 8.6.
    
    """
    def imageProc():

        return

    def dataSQL():

        return