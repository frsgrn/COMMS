from tkinter import *

class GUI():
    def __init__(self):
        self.root = Tk()
        self.centerFrame = Frame(self.root)
        self.bottomFrame = Frame(self.root)
        self.headerFrame = Frame(self.root)

        self.statusBar = Label(self.headerFrame, text="C-O-M-M-S")
        self.chatWindow = Text(self.centerFrame)
        self.inputField = Entry(self.bottomFrame)
    
    def pack(self):
        self.headerFrame.pack(side=TOP)
        self.centerFrame.pack(fill=BOTH)
        self.bottomFrame.pack(fill=X, side=BOTTOM)

        self.inputField.pack(fill=X)
        self.statusBar.pack()
        self.chatWindow.pack(fill=BOTH)