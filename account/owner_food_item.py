import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter.font import Font
from tkinter import ttk

def owner_food_item(establishment_id):
    def fetch_food_items(establishment_id, name):
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

        query = f"SELECT * FROM food_item WHERE establishment_id = {establishment_id} AND name LIKE '%{name}%'"
        database_cursor.execute(query)

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
        on_search()
    
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
        on_search()

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
        on_search()

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
        add_item_window.configure(bg="white")
        add_item_window.geometry("400x300")

        tk.Label(add_item_window, text="Name:", bg="#FFFFFF", font=("Helvetica", 8, "bold")).pack(pady=5)
        name_entry = tk.Entry(add_item_window, bd=0, bg="#FFFFFF", width=40, justify='center')
        name_entry.pack(pady=5)
        tk.Frame(add_item_window, height=2, bd=1, relief='flat', bg="#656565").pack(fill='x', padx=5)

        tk.Label(add_item_window, text="Price:", bg="#FFFFFF", font=("Helvetica", 8, "bold")).pack(pady=5)
        price_entry = tk.Entry(add_item_window, bd=0, bg="#FFFFFF", width=40, justify='center')
        price_entry.pack(pady=5)
        tk.Frame(add_item_window, height=2, bd=1, relief='flat', bg="#656565").pack(fill='x', padx=5)

        tk.Label(add_item_window, text="Description:", bg="#FFFFFF", font=("Helvetica", 8, "bold")).pack(pady=5)
        desc_entry = tk.Entry(add_item_window, bd=0, bg="#FFFFFF", width=40, justify='center')
        desc_entry.pack(pady=5)
        tk.Frame(add_item_window, height=2, bd=1, relief='flat', bg="#656565").pack(fill='x', padx=5)

        tk.Label(add_item_window, text="Food Types (comma-separated):", bg="#FFFFFF", font=("Helvetica", 8, "bold")).pack(pady=5)
        food_types_entry = tk.Entry(add_item_window, bd=0, bg="#FFFFFF", width=40, justify='center')
        food_types_entry.pack(pady=5)
        tk.Frame(add_item_window, height=2, bd=1, relief='flat', bg="#656565").pack(fill='x', padx=5)

        submit_btn = tk.Button(add_item_window, text="Submit", command=submit_item, bd=0, bg="#B46617", activebackground="#FFBA00", fg="#FFFFFF", activeforeground="#FFFFFF", cursor="hand2", width=10)
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
        on_search()

    def display_items(items):
        for widget in boxes_frame.winfo_children():
            widget.destroy()

        if not items:
            messagebox.showinfo(
                "Search Result", "No food items found for the specified establishment."
            )
            return

        row = 1
        col = 0
        for item in items:
            
            card = tk.Frame(boxes_frame, bd=1, relief="solid", padx=10, pady=10, bg="#FFFFFF")
            card.grid(row=row, column=col, padx=(60), pady=20, sticky="nsew")

            name_var = tk.StringVar(value=item[3])
            desc_var = tk.StringVar(value=item[2])
            price_var = tk.StringVar(value=f"{item[1]:.2f}")
            food_types_var = tk.StringVar(value=", ".join(get_food_types(item[0])))

            tk.Label(card, text="Name", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#B46617").pack(pady=(5, 0))
            name_entry = tk.Entry(
                card, textvariable=name_var, font=("Helvetica", 14, "bold"), state="normal", bg="#FFFFFF", fg="#FFBA00", bd=0, justify='center'
            )
            name_entry.pack(pady=(5, 0))
            tk.Frame(card, height=2, bd=1, relief='flat', bg="#656565").pack(fill='x', padx=5)

            tk.Label(card, text="Price", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#B46617").pack(pady=(5, 0))
            price_entry = tk.Entry(
                card, textvariable=price_var, font=("Helvetica", 14, "bold"), state="normal", bg="#FFFFFF", fg="#FFBA00", bd=0, justify='center'
            )
            price_entry.pack(pady=(5, 0))
            tk.Frame(card, height=2, bd=1, relief='flat', bg="#656565").pack(fill='x', padx=5)

            tk.Label(card, text="Food Types", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#B46617").pack(pady=(5, 0))
            food_types_entry = tk.Entry(
                card, textvariable=food_types_var, font=("Helvetica", 14, "bold"), state="normal", bg="#FFFFFF", fg="#FFBA00", bd=0, justify='center'
            )
            food_types_entry.pack(pady=(5, 0))
            tk.Frame(card, height=2, bd=1, relief='flat', bg="#656565").pack(fill='x', padx=5)
            
            tk.Label(
                card, 
                text="Description", 
                font=("Helvetica", 10, "bold"), 
                bg="#FFFFFF", 
                fg="#B46617"
            ).pack(pady=(5, 0))
            desc_entry = tk.Entry(
                card, textvariable=desc_var, font=("Helvetica", 8, "bold"), state="normal", bg="#FFFFFF", fg="#FFBA00", bd=0, justify='center', width=30
            )
            desc_entry.pack(pady=(5, 0))
            tk.Frame(card, height=2, bd=1, relief='flat', bg="#656565").pack(fill='x', padx=5)


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
                bg="#B46617",
                bd=0, 
                fg="#FFFFFF",
                activebackground="#FFBA00",
                activeforeground="white", 
                cursor="hand2",
                width=10,
            )
            save_btn.pack(pady=(10, 0))    

            delete_btn = tk.Button(
                card,
                text="Delete",
                command=lambda item_id=item[0]: delete_food_item(item_id),
                bg="#B46617",
                fg="#FFFFFF",
                bd=0,
                activebackground="#FFBA00",
                activeforeground="white", 
                cursor="hand2",
                width=10,
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

    def on_search():
        name = name_entry.get()
        items = fetch_food_items(establishment_id, name)
        display_items(items)

    root = tk.Toplevel()
    root.geometry("1100x600")
    root.title("Food Items")
    root.configure(bg="white")
    root.resizable(False, False)

    title_font = Font(family="Helvetica", size=20, weight="bold")
    label_font = Font(family="Helvetica", size=12, weight="bold")

    title = tk.Label(root, text="FOOD ITEMS", font=title_font, bg="white", fg="#B46617")
    title.pack(pady=10)

    search_frame = tk.Frame(root, bg="white")
    search_frame.pack(pady=10)

    name_label = tk.Label(search_frame, text="Search by Name:", font=label_font, bg="white", fg="#B46617")
    name_label.grid(row=0, column=0, padx=5)

    name_entry = tk.Entry(search_frame, bd=0, bg="#FFFFFF", width=40, justify='center')
    name_entry.grid(row=0, column=1, padx=5)
    tk.Frame(search_frame, height=2, bd=1, relief='flat', bg="#656565").grid(row=1, column=1, padx=5, sticky='ew')

    search_btn = tk.Button(search_frame, text="Search", command=on_search, bd=0, bg="#B46617", activebackground="#FFBA00", fg="#FFFFFF", activeforeground="#FFFFFF", cursor="hand2", width=10)
    search_btn.grid(row=0, column=2, padx=5)

    add_btn = tk.Button(root, text="Add Food Item", command=open_add_item_window, bd=0, bg="#B46617", activebackground="#FFBA00", fg="#FFFFFF", activeforeground="#FFFFFF", cursor="hand2", width=15)
    add_btn.pack(pady=10)

    canvas = tk.Canvas(root, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    items_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=items_frame, anchor="nw")

    boxes_frame = tk.Frame(items_frame, bg="white")
    boxes_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    on_search()

    root.mainloop()