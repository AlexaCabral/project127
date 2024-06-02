from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class ReviewWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Reviews")
        self.root.geometry("1100x550+0+90")
        self.root.resizable(False, False)
        self.root.configure(bg="white")


if __name__ == "__main__":
    root=Tk()
    obj = ReviewWindow(root)
    root.mainloop()