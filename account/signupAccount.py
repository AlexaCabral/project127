import tkinter as tk
from tkinter import messagebox
import mysql.connector
import PIL
from PIL import Image, ImageTk
import requests
from io import BytesIO

def signup(parent):
    # sign up window
    signupWindow = tk.Toplevel(parent)
    signupWindow.geometry("1100x650")
    signupWindow.title("Sign up")
    signupWindow.resizable(False, False)
    
    # back_button = tk.Button(signupWindow, text="Back", command=lambda: gotoLogIn(signupWindow, parent))
    # back_button.pack(pady=20)

def gotoLogIn(signupWindow, parent):
    signupWindow.destroy()
    
    parent.deiconify()