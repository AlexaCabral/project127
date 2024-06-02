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
#   Gray: #656565

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO
import signupAccount

# Functions
def gotoSignUp():
    root.withdraw()
    signupAccount.signup(root)
    
def email_enter(event):
    if emailEntry.get() == 'Email':
        emailEntry.delete(0, 'end')
    
def email_leave(event):
    if emailEntry.get() == '':
        emailEntry.insert(0, "Email")

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, 'end')
    passwordEntry.config(show="*")
    
def password_leave(event):
    if passwordEntry.get() == '':
        passwordEntry.insert(0, "Password")
        passwordEntry.config(show="")
        
        
def hide():
    pwBtn.config(text="Show")
    if passwordEntry.get() != "Password":
        passwordEntry.config(show="*")
    pwBtn.config(command=show)

def show():
    pwBtn.config(text="Hide")
    passwordEntry.config(show="")
    pwBtn.config(command=hide)

def login():
    email = emailEntry.get()
    password = passwordEntry.get()
    
    if (email == "" or email == "Email") or (password == "" or password == "Password"):
        messagebox.showerror("Entry error", "Invalid Email or Password.")
    
    else:
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='cyrene', database='project')
            mycursor = mydb.cursor()
            print("Connected to database...")
        except:
            messagebox.showerror("Connection", "Failed")
            return

        mycursor.execute("USE project")
        mycursor.execute("SELECT * FROM customer WHERE email=%s and password=%s",(email, password))
        
        myresult = mycursor.fetchone()
        print(myresult)
        
        if myresult == None:
            messagebox.showerror("Invalid", "Invalid Email or Password.")
        else:
            messagebox.showinfo("Log in", "Welcome.")
        

# root window
root = tk.Tk()

# window components
root.geometry("1100x650")
root.title("Log in")
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
canvas.create_rectangle(350, 25, 750, 625, fill='white', outline="#0C3B2E")

# header
label = tk.Label(canvas, text="LOGIN", font=('Courier', 30, 'bold'), bg="white", fg="#FFBA00")
label.place(x=490, y=40)

# enter email
emailEntry = tk.Entry(canvas, width=25, font=('Courier', 18, 'bold'), bd=0, fg="#656565")
emailEntry.insert(0, "Email")
emailEntry.bind("<FocusIn>", email_enter)
emailEntry.bind("<FocusOut>", email_leave)
tk.Frame(root, width=350, height=2, bg="#656565").place(x=380, y=215)
emailEntry.place(x=380, y=190)

# enter password
passwordEntry = tk.Entry(canvas, width=20, font=('Courier', 18, 'bold'), bd=0, fg="#656565")
passwordEntry.insert(0, "Password")
passwordEntry.bind("<FocusIn>", password_enter)
passwordEntry.bind("<FocusOut>", password_leave)
tk.Frame(root, width=350, height=2, bg="#656565").place(x=380, y=255)
passwordEntry.place(x=380, y=230)

# show/hide button for password
pwBtn = tk.Button(canvas, text="Show", font=('Courier', 12, 'bold'), bd=0, bg="#FFFFFF", activebackground="#FFFFFF", fg="#6D9773", activeforeground="#FF5050", cursor="hand2", command=show)
pwBtn.place(x=680, y=230)

# log in button
loginBtn = tk.Button(canvas, text="Log In", font=('Courier', 16, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=20, command=login)
loginBtn.place(x=425, y=330)

# create account
signupLabel = tk.Label(canvas, text="Don't have an account?", font=('Arial', 12), bg="white", fg="#725B32")
signupLabel.place(x=396, y=590)

# create account button
createBtn = tk.Button(canvas, text="Create an account.", font=('Arial', 11, 'bold'), bd=0, bg="#FFFFFF", activebackground="#FFFFFF", fg="#FFA500", activeforeground="#725B32", cursor="hand2", width=15, command=gotoSignUp)
createBtn.place(x=560, y=588)

root.mainloop()