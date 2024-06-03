# INSTRUCTIONS BEFORE RUNNING FILE:

# 1) Go to the path of your file e.g. "C:\Users\asus\Desktop\127\account"
# 2) Enter the ff. to ur terminal:
# ->     pip install mysql-connector-python
# ->     pip install requests pillow

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
import customer_signup_account
import owner_login_account
from customer_food_establishment import customer_food_establishment


# Functions
def go_to_signup():
    root.withdraw()
    customer_signup_account.signup(root)


def go_to_owner_login():
    root.withdraw()
    owner_login_account.new_window(root)


def email_enter(event):
    if email_entry.get() == "Email":
        email_entry.delete(0, "end")


def email_leave(event):
    if email_entry.get() == "":
        email_entry.insert(0, "Email")


def password_enter(event):
    if password_entry.get() == "Password":
        password_entry.delete(0, "end")
    password_entry.config(show="*")


def password_leave(event):
    if password_entry.get() == "":
        password_entry.insert(0, "Password")
        password_entry.config(show="")


def hide():
    password_button.config(text="Show")
    if password_entry.get() != "Password":
        password_entry.config(show="*")
    password_button.config(command=show)


def show():
    password_button.config(text="Hide")
    password_entry.config(show="")
    password_button.config(command=hide)


def login():
    email = email_entry.get()
    password = password_entry.get()

    if (email == "" or email == "Email") or (password == "" or password == "Password"):
        messagebox.showerror("Entry error", "Invalid Email or Password.")

    else:
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="chancekababy2021",
                database="project",
            )
            mycursor = mydb.cursor()
            print("Connected to database...")
        except:
            messagebox.showerror("Connection", "Failed")
            return

        mycursor.execute("USE project")
        mycursor.execute(
            "SELECT * FROM customer WHERE email=%s and password=%s", (email, password)
        )

        myresult = mycursor.fetchone()
        print(myresult)

        mycursor.close()
        mydb.close()

        if myresult == None:
            messagebox.showerror("Invalid", "Invalid Email or Password.")
            return
        
        messagebox.showinfo("Log in", "Welcome.")
        root.withdraw()
        customer_food_establishment(mycursor[0])


# root window
root = tk.Tk()

# window components
root.geometry("1100x650")
root.title("Log in")
root.resizable(False, False)  # avoid resizing window

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
canvas.create_rectangle(350, 25, 750, 625, fill="white", outline="#0C3B2E")

# header
label = tk.Label(
    canvas, text="LOGIN", font=("Courier", 30, "bold"), bg="white", fg="#FFBA00"
)
label.place(x=490, y=40)
customer_label = tk.Label(
    canvas, text="CUSTOMER", font=("Courier", 15, "bold"), bg="white", fg="#FFBA00"
)
customer_label.place(x=505, y=80)

# enter email
email_entry = tk.Entry(
    canvas, width=25, font=("Courier", 18, "bold"), bd=0, fg="#656565"
)
email_entry.insert(0, "Email")
email_entry.bind("<FocusIn>", email_enter)
email_entry.bind("<FocusOut>", email_leave)
tk.Frame(root, width=350, height=2, bg="#656565").place(x=380, y=215)
email_entry.place(x=380, y=190)

# enter password
password_entry = tk.Entry(
    canvas, width=20, font=("Courier", 18, "bold"), bd=0, fg="#656565"
)
password_entry.insert(0, "Password")
password_entry.bind("<FocusIn>", password_enter)
password_entry.bind("<FocusOut>", password_leave)
tk.Frame(root, width=350, height=2, bg="#656565").place(x=380, y=255)
password_entry.place(x=380, y=230)

# show/hide button for password
password_button = tk.Button(
    canvas,
    text="Show",
    font=("Courier", 12, "bold"),
    bd=0,
    bg="#FFFFFF",
    activebackground="#FFFFFF",
    fg="#6D9773",
    activeforeground="#FF5050",
    cursor="hand2",
    command=show,
)
password_button.place(x=680, y=230)

# log in button
login_button = tk.Button(
    canvas,
    text="Log In",
    font=("Courier", 16, "bold"),
    bd=0,
    bg="#FFBA00",
    activebackground="#FFA500",
    fg="#725B32",
    activeforeground="white",
    cursor="hand2",
    width=20,
    command=login,
)
login_button.place(x=425, y=330)

# log in as admin text
admin_label = tk.Label(
    canvas, text="Or Log in as", font=("Arial", 10), bg="white", fg="#725B32"
)
admin_label.place(x=492, y=372)

# log in as admin button
admin_button = tk.Button(
    canvas,
    text="Owner.",
    font=("Arial", 10, "bold"),
    bd=0,
    bg="#FFFFFF",
    activebackground="#FFFFFF",
    fg="#FFA500",
    activeforeground="#725B32",
    cursor="hand2",
    width=6,
    command=go_to_owner_login,
)
admin_button.place(x=566, y=371)

# create account
signup_label = tk.Label(
    canvas, text="Don't have an account?", font=("Arial", 10), bg="white", fg="#725B32"
)
signup_label.place(x=420, y=590)

# create account button
create_button = tk.Button(
    canvas,
    text="Create an account.",
    font=("Arial", 10, "bold"),
    bd=0,
    bg="#FFFFFF",
    activebackground="#FFFFFF",
    fg="#FFA500",
    activeforeground="#725B32",
    cursor="hand2",
    width=15,
    command=go_to_signup,
)
create_button.place(x=560, y=588)

root.mainloop()
