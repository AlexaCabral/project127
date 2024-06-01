import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO


def new_window(parent):
    
    # owner log in window
    newWindow = tk.Toplevel(parent)
    newWindow.geometry("1100x650")
    newWindow.title("Log in")
    newWindow.resizable(False, False)
    
    
    # access url, not relative paths
    image_url = "https://images.pexels.com/photos/1640773/pexels-photo-1640773.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    # set image as background
    response = requests.get(image_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    bg_image = ImageTk.PhotoImage(image)
    
    newWindow.bg_image = bg_image

    # canvas for newWindow
    canvas = tk.Canvas(newWindow, width=1100, height=650)
    canvas.pack(fill=tk.BOTH, expand=True)

    canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

    # sign up components
    # background
    canvas.create_rectangle(350, 25, 750, 625, fill='white', outline="#0C3B2E")
    
    # header
    label = tk.Label(canvas, text="LOG IN", font=('Courier', 30, 'bold'), bg="white", fg="#6D9773")
    label.place(x=495, y=40)
    
    createBtn = tk.Button(canvas, text="Create an account.", font=('Arial', 11, 'bold'), bd=0, bg="#FFFFFF", activebackground="#FFFFFF", fg="#6D9773", activeforeground="#0C3B2E", cursor="hand2", width=6, command=lambda: gotoLogIn(newWindow, parent))
    createBtn.place(x=601, y=588)


def gotoLogIn(newWindow, parent):
    newWindow.destroy()
    parent.deiconify()