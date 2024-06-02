import tkinter as tk
from tkinter import messagebox
import mysql.connector


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

    def add_food_item(price, description, name, establishment_id, food_types):
        print(price, description, name, establishment_id, food_types)
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

        item_id = database_cursor.lastrowid

        print(item_id)

        for food_type in food_types:
            query = (
                "INSERT INTO food_item_food_type (item_id, food_type) VALUES (%s, %s)"
            )
            database_cursor.execute(query, (item_id, food_type.strip()))
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

        query = "DELETE FROM food_item_food_type WHERE item_id = %s"
        database_cursor.execute(query, (item_id,))

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
            food_types = food_types_entry.get().split(",")
            add_food_item(price, description, name, establishment_id, food_types)
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

        tk.Label(add_item_window, text="Food Types (comma-separated):").pack(pady=5)
        food_types_entry = tk.Entry(add_item_window)
        food_types_entry.pack(pady=5)

        submit_btn = tk.Button(add_item_window, text="Submit", command=submit_item)
        submit_btn.pack(pady=20)

    def update_food_types(item_id, new_food_types):
        print(new_food_types)
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

        # Delete existing food types
        query = "DELETE FROM food_item_food_type WHERE item_id = %s"
        database_cursor.execute(query, (item_id,))
        database.commit()

        # Insert new food types
        for food_type in new_food_types:
            query = (
                "INSERT INTO food_item_food_type (item_id, food_type) VALUES (%s, %s)"
            )
            database_cursor.execute(query, (item_id, food_type.strip()))
            database.commit()

        # Closing the database connection
        database_cursor.close()
        database.close()

        # Refresh the food items list
        items = fetch_food_items(establishment_id)
        display_items(items)

    def display_items(items):
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

            name_var = tk.StringVar(value=item[3])
            desc_var = tk.StringVar(value=item[2])
            price_var = tk.StringVar(value=f"{item[1]:.2f}")
            food_types_var = tk.StringVar(value=", ".join(get_food_types(item[0])))

            tk.Label(card, text="Name:").pack(pady=(5, 0))
            name_entry = tk.Entry(
                card, textvariable=name_var, font=("Arial", 16, "bold"), state="normal"
            )
            name_entry.pack(pady=(5, 0))

            tk.Label(card, text="Description:").pack(pady=(5, 0))
            desc_entry = tk.Entry(
                card, textvariable=desc_var, font=("Arial", 12), state="normal"
            )
            desc_entry.pack(pady=(5, 0))

            tk.Label(card, text="Price:").pack(pady=(5, 0))
            price_entry = tk.Entry(
                card, textvariable=price_var, font=("Arial", 12), state="normal"
            )
            price_entry.pack(pady=(5, 0))

            tk.Label(card, text="Food Types:").pack(pady=(5, 0))
            food_types_entry = tk.Entry(
                card, textvariable=food_types_var, font=("Arial", 12), state="normal"
            )
            food_types_entry.pack(pady=(5, 0))

            def save_changes(
                item_id,
                name_var1,
                desc_var1,
                price_var1,
                food_types_var1,
                name_entry1,
                desc_entry1,
                price_entry1,
                food_types_entry1,
            ):
                new_name = name_entry1.get()
                new_desc = desc_entry1.get()
                new_price = float(price_entry1.get())
                new_food_types = food_types_entry1.get()
                update_food_item(item_id, new_price, new_desc, new_name)
                update_food_types(item_id, new_food_types.split(","))

                name_var1.set(new_name)
                desc_var1.set(new_desc)
                price_var1.set(f"{new_price:.2f}")
                food_types_var1.set(new_food_types)

            save_btn = tk.Button(
                card,
                text="Save",
                command=lambda item_id=item[
                    0
                ], name_var1=name_var, desc_var1=desc_var, price_var1=price_var, food_types_var1=food_types_var, name_entry1=name_entry, desc_entry1=desc_entry, price_entry1=price_entry, food_types_entry1=food_types_entry: save_changes(
                    item_id,
                    name_var1,
                    desc_var1,
                    price_var1,
                    food_types_var1,
                    name_entry1,
                    desc_entry1,
                    price_entry1,
                    food_types_entry1,
                ),
            )
            save_btn.pack(pady=(10, 0))

            delete_btn = tk.Button(
                card,
                text="Delete",
                command=lambda item_id=item[0]: delete_food_item(item_id),
            )
            delete_btn.pack(pady=(10, 0))

            col += 1
            if col == 3:
                col = 0
                row += 1

    def get_food_types(item_id):
        try:
            database = mysql.connector.connect(
                host="localhost",
                user="root",
                password="chancekababy2021",
                database="project",
            )
            database_cursor = database.cursor()
            query = "SELECT food_type FROM food_item_food_type WHERE item_id = %s"
            database_cursor.execute(query, (item_id,))
            food_types = [row[0] for row in database_cursor.fetchall()]
            database_cursor.close()
            database.close()
            print(food_types)
            return food_types
        except mysql.connector.Error as err:
            messagebox.showerror("Connection", f"Failed: {err}")
            return []

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
