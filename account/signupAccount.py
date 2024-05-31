import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO


def signup(parent):
    # Functions
    def name_enter(event):
        if nameEntry.get() == 'Name':
            nameEntry.delete(0, 'end')
    
    def name_leave(event):
        if nameEntry.get() == '':
            nameEntry.insert(0, "Name")
            
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
    
    def cpassword_enter(event):
        if confirmPasswordEntry.get() == 'Confirm Password':
            confirmPasswordEntry.delete(0, 'end')
        confirmPasswordEntry.config(show="*")
    
    def cpassword_leave(event):
        if confirmPasswordEntry.get() == '':
            confirmPasswordEntry.insert(0, "Confirm Password")
            confirmPasswordEntry.config(show="")
    
    def hide():
        pwBtn.config(text="Show")
        if passwordEntry.get() != "Password":
            passwordEntry.config(show="*")
        pwBtn.config(command=show)

    def show():
        pwBtn.config(text="Hide")
        passwordEntry.config(show="")
        pwBtn.config(command=hide)

    def chide():
        cpwBtn.config(text="Show")
        if confirmPasswordEntry.get() != "Confirm Password":
            confirmPasswordEntry.config(show="*")
        cpwBtn.config(command=cshow)

    def cshow():
        cpwBtn.config(text="Hide")
        confirmPasswordEntry.config(show="")
        cpwBtn.config(command=chide)
    
    def signupacc():
        name = nameEntry.get()
        email = emailEntry.get()
        password = passwordEntry.get()
        cpassword = confirmPasswordEntry.get()
        
        if (email == "" or email == "Email") or (password == "" or password == "Password") or (cpassword == "" or cpassword == "Confirm Password"):
            messagebox.showerror("Entry error", "Invalid Email or Password.")
        
        else:
            valid = 0
            if(password==cpassword):
                for char in password:
                    if char.isdigit():
                        valid = 1
                        break
                
                if valid == 0:
                    messagebox.showerror("Entry error", "Password must contain atleast one number [0-9].")
                else:
                    try:
                        mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
                        mycursor = mydb.cursor()
                        print("Connected to database...")
                    except:
                        messagebox.showerror("Connection", "Failed")
                        return

                    mycursor.execute("USE project")
                    print("projec used...")
                            
                    mycursor.execute("SELECT email FROM customer WHERE email = %s",(email,))
                    print("query")
                            
                            
                    myresult = mycursor.fetchone()
                    print(myresult)
                            
                    if myresult == (0,) or myresult == None:
                        # Insert into the database 
                        mycursor.execute("INSERT INTO customer VALUES (%s, %s, %s)", (name, password, email))
                        mycursor.commit()
                        
                        mycursor.close()
                        mydb.close()
                                
                        messagebox.showinfo("Success", "All Set! Go back and log in your account.")
                    else:
                        messagebox.showerror("Invalid!", "Account already exists!")
                        return
            else:
                messagebox.showerror("Entry error", "Invalid Email or Password.")
                return
        
    # sign up window
    signupWindow = tk.Toplevel(parent)
    signupWindow.geometry("1100x650")
    signupWindow.title("Sign up")
    signupWindow.resizable(False, False)
    
    # access url, not relative paths
    image_url = "https://images.pexels.com/photos/1640773/pexels-photo-1640773.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    # set image as background
    response = requests.get(image_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    bg_image = ImageTk.PhotoImage(image)
    
    signupWindow.bg_image = bg_image

    # canvas for signupWindow
    canvas = tk.Canvas(signupWindow, width=1100, height=650)
    canvas.pack(fill=tk.BOTH, expand=True)

    canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

    # sign up components
    # background
    canvas.create_rectangle(350, 25, 750, 625, fill='white', outline="#0C3B2E")
    
    # header
    label = tk.Label(canvas, text="SIGN UP", font=('Courier', 30, 'bold'), bg="white", fg="#FFBA00")
    label.place(x=470, y=40)
    
    # enter name
    nameEntry = tk.Entry(canvas, width=25, font=('Courier', 18, 'bold'), bd=0, fg="#656565")
    nameEntry.insert(0, "Name")
    nameEntry.bind("<FocusIn>", name_enter)
    nameEntry.bind("<FocusOut>", name_leave)
    tk.Frame(signupWindow, width=350, height=2, bg="#656565").place(x=380, y=215)
    nameEntry.place(x=380, y=190)
    
    # enter email
    emailEntry = tk.Entry(canvas, width=25, font=('Courier', 18, 'bold'), bd=0, fg="#656565")
    emailEntry.insert(0, "Email")
    emailEntry.bind("<FocusIn>", email_enter)
    emailEntry.bind("<FocusOut>", email_leave)
    tk.Frame(signupWindow, width=350, height=2, bg="#656565").place(x=380, y=255)
    emailEntry.place(x=380, y=230)
    
    # enter password
    passwordEntry = tk.Entry(canvas, width=20, font=('Courier', 18, 'bold'), bd=0, fg="#656565")
    passwordEntry.insert(0, "Password")
    passwordEntry.bind("<FocusIn>", password_enter)
    passwordEntry.bind("<FocusOut>", password_leave)
    tk.Frame(signupWindow, width=350, height=2, bg="#656565").place(x=380, y=295)
    passwordEntry.place(x=380, y=270)
    
    # confirm password
    confirmPasswordEntry = tk.Entry(canvas, width=20, font=('Courier', 18, 'bold'), bd=0, fg="#656565")
    confirmPasswordEntry.insert(0, "Confirm Password")
    confirmPasswordEntry.bind("<FocusIn>", cpassword_enter)
    confirmPasswordEntry.bind("<FocusOut>", cpassword_leave)
    tk.Frame(signupWindow, width=350, height=2, bg="#656565").place(x=380, y=335)
    confirmPasswordEntry.place(x=380, y=310)
    
    # show/hide button for password
    pwBtn = tk.Button(canvas, text="Show", font=('Courier', 12, 'bold'), bd=0, bg="#FFFFFF", activebackground="#FFFFFF", fg="#6D9773", activeforeground="#FF5050", cursor="hand2", command=show)
    pwBtn.place(x=680, y=270)
    
    # show/hide button for password
    cpwBtn = tk.Button(canvas, text="Show", font=('Courier', 12, 'bold'), bd=0, bg="#FFFFFF", activebackground="#FFFFFF", fg="#6D9773", activeforeground="#FF5050", cursor="hand2", command=cshow)
    cpwBtn.place(x=680, y=310)
    
    # sign up button
    signupBtn = tk.Button(canvas, text="Sign Up", font=('Courier', 16, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=20, command=signupacc)
    signupBtn.place(x=420, y=430)
    
    # go back to log in account
    loginLabel = tk.Label(canvas, text="Already have an account?", font=('Arial', 12), bg="white", fg="#725B32")
    loginLabel.place(x=420, y=590)

    createBtn = tk.Button(canvas, text="Log in.", font=('Arial', 11, 'bold'), bd=0, bg="#FFFFFF", activebackground="#FFFFFF", fg="#FFA500", activeforeground="#725B32", cursor="hand2", width=6, command=lambda: gotoLogIn(signupWindow, parent))
    createBtn.place(x=601, y=588)
    
    # backBtn = tk.Button(canvas, text="Go back to Log in page", command=lambda: gotoLogIn(signupWindow, parent))
    # backBtn.pack(pady=20)

def gotoLogIn(signupWindow, parent):
    signupWindow.destroy()
    parent.deiconify()