# INSTRUCTIONS BEFORE RUNNING FILE:

# 1) Go to the path of your file e.g. "C:\Users\asus\Desktop\127\account"
# 2) Enter the ff. to ur terminal:
#->     pip install mysql-connector-python
#->     pip install requests pillow

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO

root = tk.Tk()

# window elements
root.geometry("1100x650")
root.title("Login")
root.resizable(False, False)    # avoid resizing window

# access url, not relative paths
image_url = "https://images.pexels.com/photos/1640774/pexels-photo-1640774.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

# set image as background
response = requests.get(image_url)
image_data = response.content
image = Image.open(BytesIO(image_data))
# image = image.resize((1100, 650), PIL.Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(image)

# canvas for root
canvas = tk.Canvas(root, width=1100, height=650)
canvas.pack(fill=tk.BOTH, expand=True)

canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

root.mainloop()