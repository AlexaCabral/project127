import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO
import owner_signup_account
from owner_food_establishment import owner_food_establishment


def new_window(parent):
    def gotoSignUp():
        newWindow.withdraw()
        owner_signup_account.signup(newWindow)

    def email_enter(event):
        if emailEntry.get() == "Email":
            emailEntry.delete(0, "end")

    def email_leave(event):
        if emailEntry.get() == "":
            emailEntry.insert(0, "Email")

    def password_enter(event):
        if passwordEntry.get() == "Password":
            passwordEntry.delete(0, "end")
        passwordEntry.config(show="*")

    def password_leave(event):
        if passwordEntry.get() == "":
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

        if (email == "" or email == "Email") or (
            password == "" or password == "Password"
        ):
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
                "SELECT * FROM owner WHERE email=%s and password=%s", (email, password)
            )

            myresult = mycursor.fetchone()
            print(myresult)

            if myresult == None:
                messagebox.showerror("Invalid", "Invalid Email or Password.")
            else:
                messagebox.showinfo("Log in", "Welcome.")
                parent.destroy()  # Close the login window
                mycursor.execute(
                    "SELECT account_id FROM owner WHERE email=%s and password=%s",
                    (email, password),
                )
                account_id = mycursor.fetchone()[0]
                owner_food_establishment(account_id)  # Open the customer food establishment window

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
    canvas.create_rectangle(350, 25, 750, 625, fill="white", outline="#0C3B2E")

    # header
    label = tk.Label(
        canvas, text="LOGIN", font=("Courier", 30, "bold"), bg="white", fg="#6D9773"
    )
    label.place(x=490, y=40)
    labelowner = tk.Label(
        canvas, text="OWNER", font=("Courier", 15, "bold"), bg="white", fg="#6D9773"
    )
    labelowner.place(x=520, y=80)

    # enter email
    emailEntry = tk.Entry(
        canvas, width=25, font=("Courier", 18, "bold"), bd=0, fg="#656565"
    )
    emailEntry.insert(0, "Email")
    emailEntry.bind("<FocusIn>", email_enter)
    emailEntry.bind("<FocusOut>", email_leave)
    tk.Frame(newWindow, width=350, height=2, bg="#656565").place(x=380, y=215)
    emailEntry.place(x=380, y=190)

    # enter password
    passwordEntry = tk.Entry(
        canvas, width=20, font=("Courier", 18, "bold"), bd=0, fg="#656565"
    )
    passwordEntry.insert(0, "Password")
    passwordEntry.bind("<FocusIn>", password_enter)
    passwordEntry.bind("<FocusOut>", password_leave)
    tk.Frame(newWindow, width=350, height=2, bg="#656565").place(x=380, y=255)
    passwordEntry.place(x=380, y=230)

    # show/hide button for password
    pwBtn = tk.Button(
        canvas,
        text="Show",
        font=("Courier", 12, "bold"),
        bd=0,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        fg="#FFBA00",
        activeforeground="#FF5050",
        cursor="hand2",
        command=show,
    )
    pwBtn.place(x=680, y=230)

    # log in button
    loginBtn = tk.Button(
        canvas,
        text="Log In",
        font=("Courier", 16, "bold"),
        bd=0,
        bg="#6D9773",
        activebackground="#0C3B2E",
        fg="#2E4D3D",
        activeforeground="white",
        cursor="hand2",
        width=20,
        command=login,
    )
    loginBtn.place(x=425, y=330)

    # log in as customer text
    customerLabel = tk.Label(
        canvas, text="Or Log in as", font=("Arial", 10), bg="white", fg="#0C3B2E"
    )
    customerLabel.place(x=492, y=372)

    # log in as customer button
    customerBtn = tk.Button(
        canvas,
        text="Customer.",
        font=("Arial", 10, "bold"),
        bd=0,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        fg="#6D9773",
        activeforeground="#0C3B2E",
        cursor="hand2",
        width=8,
        command=lambda: gotoLogIn(newWindow, parent),
    )
    customerBtn.place(x=566, y=371)

    # create account
    signupLabel = tk.Label(
        canvas,
        text="Don't have an account?",
        font=("Arial", 10),
        bg="white",
        fg="#0C3B2E",
    )
    signupLabel.place(x=420, y=590)

    # create button
    createBtn = tk.Button(
        canvas,
        text="Create an account.",
        font=("Arial", 10, "bold"),
        bd=0,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        fg="#6D9773",
        activeforeground="#0C3B2E",
        cursor="hand2",
        width=15,
        command=gotoSignUp,
    )
    createBtn.place(x=560, y=588)


def gotoLogIn(newWindow, parent):
    newWindow.destroy()
    parent.deiconify()
