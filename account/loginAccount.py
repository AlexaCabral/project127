# INSTRUCTIONS BEFORE RUNNING FILE:

# 1) Go to the path of your file e.g. "C:\Users\asus\Desktop\127\account"
# 2) Enter the ff. to ur terminal:
#->     pip install mysql-connector-python
#->     pip install requests pillow

#   COLOR PALETTE:
#   Yellow: #FFBA00
#   Dark Orange: #B46617
#   Dark Green: #0C3B2E
#   Light Green: #6D9773

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Functions
def email_enter(event):
    if emailEntry.get() == 'Email':
        emailEntry.delete(0, 'end')
    
def email_leave(event):
    if emailEntry.get() == '':
        emailEntry.insert(0, "Email")

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, 'end')
    
def password_leave(event):
    if passwordEntry.get() == '':
        passwordEntry.insert(0, "Password")

# root window
root = tk.Tk()

# window components
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




# log in components
# background
canvas.create_rectangle(300, 25, 800, 625, fill='white', outline="#0C3B2E")

# header
label = tk.Label(canvas, text="LOGIN", font=('Courier', 30, 'bold'), bg="white", fg="#FFBA00")
label.place(x=490, y=40)

# enter email
emailEntry = tk.Entry(canvas, width=25, font=('Courier', 18, 'bold'), bd=0, fg="#FFBA00")
emailEntry.insert(0, "Email")
emailEntry.bind("<FocusIn>", email_enter)
emailEntry.bind("<FocusOut>", email_leave)
tk.Frame(root, width=350, height=2, bg="#FFBA00").place(x=380, y=215)
emailEntry.place(x=380, y=190)

# enter password
passwordEntry = tk.Entry(canvas, width=25, font=('Courier', 18, 'bold'), bd=0, fg="#FFBA00")
passwordEntry.insert(0, "Password")
passwordEntry.bind("<FocusIn>", password_enter)
passwordEntry.bind("<FocusOut>", password_leave)
tk.Frame(root, width=350, height=2, bg="#FFBA00").place(x=380, y=255)
passwordEntry.place(x=380, y=230)


root.mainloop()