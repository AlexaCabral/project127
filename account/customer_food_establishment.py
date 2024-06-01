import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading


def customer_food_establishment():
    def search_food_establishment(name):
        try:
            database = mysql.connector.connect(
                host="localhost",
                user="root",
                password="chancekababy2021",
                database="project",
            )
            database_cursor = database.cursor()
            print("Connected to database...")
        except mysql.connector.Error as err:
            messagebox.showerror("Connection", f"Failed: {err}")
            return []

        query = "SELECT * FROM food_establishment WHERE name LIKE %s"
        database_cursor.execute(query, (f"%{name}%",))

        results = database_cursor.fetchall()

        # Closing the database connection
        database_cursor.close()
        database.close()

        return results

    def download_image(image_url, callback):
        try:
            response = requests.get(image_url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            callback(photo)
        except Exception as e:
            print(f"Failed to download image: {e}")

    def display_results(name):
        results = search_food_establishment(name)

        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()

        if not results:
            messagebox.showinfo(
                "Search Result", "No food establishments found with the specified name."
            )
            return

        row = 1
        col = 0
        for est in results:
            card = tk.Frame(results_frame, bd=2, relief="solid", padx=10, pady=10)
            card.grid(row=row, column=col, padx=10, pady=10)

            # Placeholder for the image
            img_label = tk.Label(card)
            img_label.pack()

            def update_image(photo, img_label=img_label):
                img_label.config(image=photo)
                img_label.image = photo

            image_url = "https://via.placeholder.com/150"
            threading.Thread(
                target=download_image, args=(image_url, update_image)
            ).start()

            name_label = tk.Label(card, text=est[4], font=("Arial", 16, "bold"))
            name_label.pack(pady=(10, 0))

            desc_label = tk.Label(
                card, text=est[2], font=("Arial", 12), wraplength=200, justify="left"
            )
            desc_label.pack(pady=(10, 0))

            rating_label = tk.Label(card, text=f"Rating: {est[3]}", font=("Arial", 12))
            rating_label.pack(pady=(10, 0))

            col += 1
            if col == 3:
                col = 0
                row += 1

    def on_search():
        name = search_entry.get()
        display_results(name)

    # Root window setup
    root = tk.Tk()
    root.title("Food Establishment Search")
    root.geometry("1100x650")

    # Search bar
    search_frame = tk.Frame(root, bg="#d9c3ac")
    search_frame.pack(fill=tk.X, pady=20)

    tk.Label(
        search_frame, text="REVIEW127", font=("Arial", 24, "bold"), bg="#d9c3ac"
    ).pack(side=tk.LEFT, padx=10)
    search_entry = tk.Entry(search_frame, font=("Arial", 14), width=50)
    search_entry.pack(side=tk.LEFT, padx=10)
    search_btn = tk.Button(
        search_frame, text="Search", font=("Arial", 14), command=on_search, bg="#d9c3ac"
    )
    search_btn.pack(side=tk.LEFT, padx=10)

    # Results frame
    results_frame = tk.Frame(root)
    results_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    root.mainloop()


customer_food_establishment()
