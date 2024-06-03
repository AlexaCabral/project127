import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re


def signup(parent):
    # Functions
    def name_enter(event):
        if name_entry.get() == "Name":
            name_entry.delete(0, "end")

    def name_leave(event):
        if name_entry.get() == "":
            name_entry.insert(0, "Name")

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

    def confirm_password_enter(event):
        if confirm_password_entry.get() == "Confirm Password":
            confirm_password_entry.delete(0, "end")
        confirm_password_entry.config(show="*")

    def confirm_password_leave(event):
        if confirm_password_entry.get() == "":
            confirm_password_entry.insert(0, "Confirm Password")
            confirm_password_entry.config(show="")

    def hide():
        password_button.config(text="Show")
        if password_entry.get() != "Password":
            password_entry.config(show="*")
        password_button.config(command=show)

    def show():
        password_button.config(text="Hide")
        password_entry.config(show="")
        password_button.config(command=hide)

    def confirm_password_hide():
        confirm_password_button.config(text="Show")
        if confirm_password_entry.get() != "Confirm Password":
            confirm_password_entry.config(show="*")
        confirm_password_button.config(command=confirm_password_show)

    def confirm_password_show():
        confirm_password_button.config(text="Hide")
        confirm_password_entry.config(show="")
        confirm_password_button.config(command=confirm_password_hide)

    def is_email_valid(email):
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        return re.match(pattern, email) is not None

    def signup_account():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if (
            (email == "" or email == "Email")
            or (password == "" or password == "Password")
            or (confirm_password == "" or confirm_password == "Confirm Password")
        ):
            messagebox.showerror("Entry error", "Invalid Email or Password.")

        else:
            pvalid = 0

            if password == confirm_password:
                for char in password:
                    if char.isdigit():
                        pvalid = 1
                        break

                if pvalid == 0:
                    messagebox.showerror(
                        "Entry error", "Password must contain atleast one number [0-9]."
                    )

                else:
                    if not is_email_valid(email):
                        messagebox.showerror(
                            "Entry error", "Email must follow the format: __@__.__"
                        )
                        return
                    else:
                        try:
                            mydb = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="server",
                                database="project",
                            )
                            mycursor = mydb.cursor()
                            print("Connected to database...")
                        except:
                            messagebox.showerror("Connection", "Failed")
                            return

                        mycursor.execute("USE project")
                        print("project used...")

                        mycursor.execute(
                            "SELECT COUNT(*) FROM customer WHERE email = %s", (email,)
                        )
                        print("query")

                        myresult = mycursor.fetchone()[0]
                        print(myresult)

                        if myresult == 0:
                            # Insert into the database
                            mycursor.execute(
                                "INSERT INTO customer(name, password, email) VALUES (%s, %s, %s)",
                                (name, password, email),
                            )

                            mydb.commit()

                            messagebox.showinfo(
                                "Success", "All Set! Go back and log into your account."
                            )
                        else:
                            messagebox.showerror("Invalid!", "Account already exists!")
                            return

    # sign up window
    signup_window = tk.Toplevel(parent)
    signup_window.geometry("1100x650")
    signup_window.title("Sign up")
    signup_window.resizable(False, False)

    # access url, not relative paths
    image_url = "https://images.pexels.com/photos/1640773/pexels-photo-1640773.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    # set image as background
    response = requests.get(image_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    bg_image = ImageTk.PhotoImage(image)

    signup_window.bg_image = bg_image

    # canvas for signup_window
    canvas = tk.Canvas(signup_window, width=1100, height=650)
    canvas.pack(fill=tk.BOTH, expand=True)

    canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

    # sign up components
    # background
    canvas.create_rectangle(350, 25, 750, 625, fill="white", outline="#0C3B2E")

    # header
    label = tk.Label(
        canvas, text="SIGN UP", font=("Courier", 30, "bold"), bg="white", fg="#FFBA00"
    )
    label.place(x=470, y=40)
    customer_label = tk.Label(
        canvas, text="CUSTOMER", font=("Courier", 15, "bold"), bg="white", fg="#FFBA00"
    )
    customer_label.place(x=505, y=80)

    # enter name
    name_entry = tk.Entry(
        canvas, width=25, font=("Courier", 18, "bold"), bd=0, fg="#656565"
    )
    name_entry.insert(0, "Name")
    name_entry.bind("<FocusIn>", name_enter)
    name_entry.bind("<FocusOut>", name_leave)
    tk.Frame(signup_window, width=350, height=2, bg="#656565").place(x=380, y=215)
    name_entry.place(x=380, y=190)

    # enter email
    email_entry = tk.Entry(
        canvas, width=25, font=("Courier", 18, "bold"), bd=0, fg="#656565"
    )
    email_entry.insert(0, "Email")
    email_entry.bind("<FocusIn>", email_enter)
    email_entry.bind("<FocusOut>", email_leave)
    tk.Frame(signup_window, width=350, height=2, bg="#656565").place(x=380, y=255)
    email_entry.place(x=380, y=230)

    # enter password
    password_entry = tk.Entry(
        canvas, width=20, font=("Courier", 18, "bold"), bd=0, fg="#656565"
    )
    password_entry.insert(0, "Password")
    password_entry.bind("<FocusIn>", password_enter)
    password_entry.bind("<FocusOut>", password_leave)
    tk.Frame(signup_window, width=350, height=2, bg="#656565").place(x=380, y=295)
    password_entry.place(x=380, y=270)

    # confirm password
    confirm_password_entry = tk.Entry(
        canvas, width=20, font=("Courier", 18, "bold"), bd=0, fg="#656565"
    )
    confirm_password_entry.insert(0, "Confirm Password")
    confirm_password_entry.bind("<FocusIn>", confirm_password_enter)
    confirm_password_entry.bind("<FocusOut>", confirm_password_leave)
    tk.Frame(signup_window, width=350, height=2, bg="#656565").place(x=380, y=335)
    confirm_password_entry.place(x=380, y=310)

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
    password_button.place(x=680, y=270)

    # show/hide button for password
    confirm_password_button = tk.Button(
        canvas,
        text="Show",
        font=("Courier", 12, "bold"),
        bd=0,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        fg="#6D9773",
        activeforeground="#FF5050",
        cursor="hand2",
        command=confirm_password_show,
    )
    confirm_password_button.place(x=680, y=310)

    # sign up button
    signup_button = tk.Button(
        canvas,
        text="Sign Up",
        font=("Courier", 16, "bold"),
        bd=0,
        bg="#FFBA00",
        activebackground="#FFA500",
        fg="#725B32",
        activeforeground="white",
        cursor="hand2",
        width=20,
        command=signup_account,
    )
    signup_button.place(x=420, y=430)

    # go back to log in account
    login_label = tk.Label(
        canvas,
        text="Already have an account?",
        font=("Arial", 12),
        bg="white",
        fg="#725B32",
    )
    login_label.place(x=420, y=590)

    create_button = tk.Button(
        canvas,
        text="Log in.",
        font=("Arial", 11, "bold"),
        bd=0,
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        fg="#FFA500",
        activeforeground="#725B32",
        cursor="hand2",
        width=6,
        command=lambda: go_to_login(signup_window, parent),
    )
    create_button.place(x=601, y=588)


def go_to_login(signup_window, parent):
    signup_window.destroy()
    parent.deiconify()
