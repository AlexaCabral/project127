import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO
import owner_signup_account
from reports import MainSystem


def new_window(parent):
    def go_to_signup():
        new_window.withdraw()
        owner_signup_account.signup(new_window)

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

        if (email == "" or email == "Email") or (
            password == "" or password == "Password"
        ):
            messagebox.showerror("Entry error", "Invalid Email or Password.")
            return

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
            return

        messagebox.showinfo("Log in", "Welcome.")
        new_window.withdraw()
        new_root = tk.Tk()
        MainSystem(new_root, user_type="owner", account_id=myresult[0])
        new_root.mainloop()

    # owner log in window
    new_window = tk.Toplevel(parent)
    new_window.geometry("1100x650")
    new_window.title("Log in")
    new_window.resizable(False, False)

    # access url, not relative paths
    image_url = "https://images.pexels.com/photos/1640773/pexels-photo-1640773.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    # set image as background
    response = requests.get(image_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    background_image = ImageTk.PhotoImage(image)

    new_window.bg_image = background_image

    # canvas for new_window
    canvas = tk.Canvas(new_window, width=1100, height=650)
    canvas.pack(fill=tk.BOTH, expand=True)

    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

    # sign up components
    # background
    canvas.create_rectangle(350, 25, 750, 625, fill="white", outline="#0C3B2E")

    # header
    label = tk.Label(
        canvas, text="LOGIN", font=("Courier", 30, "bold"), bg="white", fg="#6D9773"
    )
    label.place(x=490, y=40)
    owner_label = tk.Label(
        canvas, text="OWNER", font=("Courier", 15, "bold"), bg="white", fg="#6D9773"
    )
    owner_label.place(x=520, y=80)

    # enter email
    email_entry = tk.Entry(
        canvas, width=25, font=("Courier", 18, "bold"), bd=0, fg="#656565"
    )
    email_entry.insert(0, "Email")
    email_entry.bind("<FocusIn>", email_enter)
    email_entry.bind("<FocusOut>", email_leave)
    tk.Frame(new_window, width=350, height=2, bg="#656565").place(x=380, y=215)
    email_entry.place(x=380, y=190)

    # enter password
    password_entry = tk.Entry(
        canvas, width=20, font=("Courier", 18, "bold"), bd=0, fg="#656565"
    )
    password_entry.insert(0, "Password")
    password_entry.bind("<FocusIn>", password_enter)
    password_entry.bind("<FocusOut>", password_leave)
    tk.Frame(new_window, width=350, height=2, bg="#656565").place(x=380, y=255)
    password_entry.place(x=380, y=230)

    # show/hide button for password
    password_button = tk.Button(
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
    password_button.place(x=680, y=230)

    # log in button
    login_button = tk.Button(
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
    login_button.place(x=425, y=330)

    # log in as customer text
    customer_label = tk.Label(
        canvas, text="Or Log in as", font=("Arial", 10), bg="white", fg="#0C3B2E"
    )
    customer_label.place(x=492, y=372)

    # log in as customer button
    customer_button = tk.Button(
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
        command=lambda: go_to_login(new_window, parent),
    )
    customer_button.place(x=566, y=371)

    # create account
    signup_label = tk.Label(
        canvas,
        text="Don't have an account?",
        font=("Arial", 10),
        bg="white",
        fg="#0C3B2E",
    )
    signup_label.place(x=420, y=590)

    # create button
    create_button = tk.Button(
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
        command=go_to_signup,
    )
    create_button.place(x=560, y=588)


def go_to_login(new_window, parent):
    new_window.destroy()
    parent.deiconify()
