import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading


def owner_food_item(establishment_id):
    def fetch_food_items(establishment_id):
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

        query = "SELECT * FROM food_item WHERE establishment_id = %s"
        database_cursor.execute(query, (establishment_id,))

        results = database_cursor.fetchall()

        # Closing the database connection
        database_cursor.close()
        database.close()

        return results

    def add_food_item(price, description, name, establishment_id):
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
            return

        query = "INSERT INTO food_item (price, description, name, establishment_id) VALUES (%s, %s, %s, %s)"
        database_cursor.execute(query, (price, description, name, establishment_id))
        database.commit()

        # Closing the database connection
        database_cursor.close()
        database.close()

        # Refresh the food items list
        items = fetch_food_items(establishment_id)
        display_items(items)

    def update_food_item(item_id, price, description, name):
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
            return

        query = "UPDATE food_item SET price = %s, description = %s, name = %s WHERE item_id = %s"
        database_cursor.execute(query, (price, description, name, item_id))
        database.commit()

        # Closing the database connection
        database_cursor.close()
        database.close()

        # Refresh the food items list
        items = fetch_food_items(establishment_id)
        display_items(items)

    def delete_food_item(item_id):
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
            return

        query = "DELETE FROM food_item WHERE item_id = %s"
        database_cursor.execute(query, (item_id,))
        database.commit()

        # Closing the database connection
        database_cursor.close()
        database.close()

        # Refresh the food items list
        items = fetch_food_items(establishment_id)
        display_items(items)

    def open_add_item_window():
        def submit_item():
            price = price_entry.get()
            description = desc_entry.get()
            name = name_entry.get()
            add_food_item(price, description, name, establishment_id)
            add_item_window.destroy()

        add_item_window = tk.Toplevel(root)
        add_item_window.title("Add Food Item")

        tk.Label(add_item_window, text="Price:").pack(pady=5)
        price_entry = tk.Entry(add_item_window)
        price_entry.pack(pady=5)

        tk.Label(add_item_window, text="Description:").pack(pady=5)
        desc_entry = tk.Entry(add_item_window)
        desc_entry.pack(pady=5)

        tk.Label(add_item_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_item_window)
        name_entry.pack(pady=5)

        submit_btn = tk.Button(add_item_window, text="Submit", command=submit_item)
        submit_btn.pack(pady=20)

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

    def display_items(items):
        # Clear previous items
        for widget in items_frame.winfo_children():
            widget.destroy()

        if not items:
            messagebox.showinfo(
                "Search Result", "No food items found for the specified establishment."
            )
            return

        row = 1
        col = 0
        for item in items:
            card = tk.Frame(items_frame, bd=2, relief="solid", padx=10, pady=10)
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

            name_var = tk.StringVar(value=item[3])
            desc_var = tk.StringVar(value=item[2])
            price_var = tk.StringVar(value=f"{item[1]:.2f}")

            name_label = tk.Label(card, textvariable=name_var, font=("Arial", 16, "bold"))
            name_label.pack(pady=(10, 0))

            desc_label = tk.Label(
                card, textvariable=desc_var, font=("Arial", 12), wraplength=200, justify="left"
            )
            desc_label.pack(pady=(10, 0))

            price_label = tk.Label(card, text=f"Price: ${price_var.get()}", font=("Arial", 12))
            price_label.pack(pady=(10, 0))

            def toggle_edit():
                if edit_btn['text'] == 'Edit':
                    name_entry = tk.Entry(card, textvariable=name_var, font=("Arial", 16, "bold"))
                    name_entry.pack(pady=(10, 0))
                    desc_entry = tk.Entry(card, textvariable=desc_var, font=("Arial", 12))
                    desc_entry.pack(pady=(10, 0))
                    price_entry = tk.Entry(card, textvariable=price_var, font=("Arial", 12))
                    price_entry.pack(pady=(10, 0))

                    name_label.pack_forget()
                    desc_label.pack_forget()
                    price_label.pack_forget()

                    edit_btn.config(text='Save', command=lambda: save_changes(item[0], name_entry, desc_entry, price_entry, name_label, desc_label, price_label))
                else:
                    save_changes(item[0], name_entry, desc_entry, price_entry, name_label, desc_label, price_label)

            def save_changes(item_id, name_entry, desc_entry, price_entry, name_label, desc_label, price_label):
                new_name = name_entry.get()
                new_desc = desc_entry.get()
                new_price = float(price_entry.get())
                update_food_item(item_id, new_price, new_desc, new_name)

                name_var.set(new_name)
                desc_var.set(new_desc)
                price_var.set(f"{new_price:.2f}")

                name_entry.pack_forget()
                desc_entry.pack_forget()
                price_entry.pack_forget()

                name_label.pack(pady=(10, 0))
                desc_label.pack(pady=(10, 0))
                price_label.config(text=f"Price: ${new_price:.2f}")
                price_label.pack(pady=(10, 0))

                edit_btn.config(text='Edit', command=toggle_edit)

            edit_btn = tk.Button(card, text="Edit", command=toggle_edit)
            edit_btn.pack(pady=(10, 0))

            delete_btn = tk.Button(card, text="Delete", command=lambda item_id=item[0]: delete_food_item(item_id))
            delete_btn.pack(pady=(10, 0))

            col += 1
            if col == 3:
                col = 0
                row += 1

    # Root window setup
    root = tk.Toplevel()
    root.title("Food Items")
    root.geometry("1100x650")

    # Items frame
    items_frame = tk.Frame(root)
    items_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    items = fetch_food_items(establishment_id)
    display_items(items)

    # Add Food Item button
    add_item_btn = tk.Button(root, text="Add Food Item", command=open_add_item_window)
    add_item_btn.pack(pady=10)

    root.mainloop()
