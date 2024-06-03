import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import estabReviews
from owner_food_item import owner_food_item

def owner_food_establishment(account_id):
    # Function to establish a database connection
    def connect_to_db():
        try:
            database = mysql.connector.connect(
                host="localhost",
                user="root",
                password="cyrene",
                database="project",
            )
            print("Connected to database...")
            return database
        except mysql.connector.Error as err:
            messagebox.showerror("Connection", f"Failed: {err}")
            return None

    # Function to search food establishments
    def search_food_establishment(name):
        database = connect_to_db()
        if not database:
            return []

        database_cursor = database.cursor()
        query = f"SELECT * FROM food_establishment WHERE account_id={account_id} AND name LIKE '%{name}%'"
        print(query)
        database_cursor.execute(query)
        results = database_cursor.fetchall()
        database_cursor.close()
        database.close()
        return results

    # Function to add a new food establishment
    def add_item():
        dialog = AddItemDialog(foodestabWindow)
        foodestabWindow.wait_window(dialog.top)
        if dialog.result:
            database = connect_to_db()
            if not database:
                return
            database_cursor = database.cursor()
            query = (
                "INSERT INTO food_establishment (location, description, average_rating, name, account_id) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            values = (
                dialog.result["location"],
                dialog.result["description"],
                0,
                dialog.result["name"],
                account_id,
            )
            database_cursor.execute(query, values)
            database.commit()
            dialog.result["estab_id"] = database_cursor.lastrowid
            database_cursor.close()
            database.close()
            create_new_box(dialog.result)

    class AddItemDialog:
        def __init__(self, parent):
            self.top = tk.Toplevel(parent)
            self.top.title("Add New Item")
            self.top.geometry("300x200")
            self.result = None

            tk.Label(self.top, text="Establishment Name:", foreground="#B46617", font=("Helvetica", 12, "bold")).pack()
            self.estab_name_entry = ttk.Entry(self.top, foreground="black", font=("Helvetica", 11))
            self.estab_name_entry.pack()

            tk.Label(self.top, text="Location:", foreground="#B46617", font=("Helvetica", 12, "bold")).pack()
            self.location_entry = ttk.Entry(self.top, foreground="black", font=("Helvetica", 11))
            self.location_entry.pack()

            tk.Label(self.top, text="Description:", foreground="#B46617", font=("Helvetica", 12, "bold")).pack()
            self.description_entry = ttk.Entry(self.top, foreground="black", font=("Helvetica", 11))
            self.description_entry.pack()

            tk.Button(self.top, text="Add", command=self.add, font=("Helvetica", 10, "bold"), fg="white", bg="#B46617", activebackground="#FFBA00", activeforeground="white").pack()

        def add(self):
            self.result = {
                "name": self.estab_name_entry.get(),
                "location": self.location_entry.get(),
                "description": self.description_entry.get(),
            }
            self.top.destroy()

    class EditItemDialog:
        def __init__(self, parent, item):
            self.top = tk.Toplevel(parent)
            self.top.title("Edit Item")
            self.top.geometry("300x200")
            self.result = None

            tk.Label(self.top, text="Establishment Name:", foreground="#B46617", font=("Helvetica", 12, "bold")).pack()
            self.estab_name_entry = ttk.Entry(self.top, foreground="black", font=("Helvetica", 11))
            self.estab_name_entry.pack()
            self.estab_name_entry.insert(0, item["name"])

            tk.Label(self.top, text="Location:", foreground="#B46617", font=("Helvetica", 12, "bold")).pack()
            self.location_entry = ttk.Entry(self.top, foreground="black", font=("Helvetica", 11))
            self.location_entry.pack()
            self.location_entry.insert(0, item["location"])

            tk.Label(self.top, text="Description:", foreground="#B46617", font=("Helvetica", 12, "bold")).pack()
            self.description_entry = ttk.Entry(self.top, foreground="black", font=("Helvetica", 11))
            self.description_entry.pack()
            self.description_entry.insert(0, item["description"])

            button = tk.Button(self.top, text="Update", command=self.update, font=("Helvetica", 10, "bold"), fg="white", bg="#B46617")
            button.pack()

        def update(self):
            self.result = {
                "name": self.estab_name_entry.get(),
                "location": self.location_entry.get(),
                "description": self.description_entry.get(),
            }
            self.top.destroy()

    def create_new_box(establishment):
        ttk.Style().configure("Custom.TFrame", background="white", font=("Helvetica", 10, "bold"))
        style = ttk.Style()
        style.configure("Green.TButton", background="#B46617", foreground="#B46617", font=("Helvetica", 10, "bold"))

        new_box_frame = ttk.Frame(boxes_frame, borderwidth=1, relief="solid", style="Custom.TFrame")

        total_boxes = len([child for child in boxes_frame.grid_slaves() if isinstance(child, ttk.Frame)])

        row_position = total_boxes // 3
        column_position = total_boxes % 3

        padx_value = 10
        pady_value = 10

        new_box_frame.grid(row=row_position, column=column_position, padx=padx_value, pady=pady_value, sticky="nsew")

        item_name_label = tk.Label(new_box_frame, text=establishment["name"].strip(), bg="white", font=("Helvetica", 20, "bold"), foreground="#FFA500")
        item_name_label.pack(expand=True, pady=10)

        details_frame = tk.Frame(new_box_frame, bg="white")
        details_frame.pack(expand=True, pady=2)

        # Create labels for each piece of information
        labels = [
            ("ID:", establishment['estab_id']),
            ("Location:", establishment['location']),
            ("Description:", establishment['description'])
        ]

        # Iterate through the labels and add them to the grid
        for i, (label_text, value) in enumerate(labels):
            label_key = tk.Label(details_frame, text=label_text, font=("Helvetica", 14), fg="#B46617", bg="white")
            label_value = tk.Label(details_frame, text=value, font=("Helvetica", 14), fg="black", bg="white")

            label_key.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            label_value.grid(row=i, column=1, sticky="w", padx=5, pady=2)

        edit_delete_frame = tk.Frame(new_box_frame, bg="white")
        edit_delete_frame.pack()

        edit_button = tk.Button(
            edit_delete_frame,
            text="Edit",
            command=lambda: edit_item(new_box_frame, establishment),
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#B46617",
            bd=0,
            activebackground="#FFA500",
            activeforeground="white",
            cursor="hand2",
            width=7,
        )
        edit_button.pack(side="left", padx=3, pady=2)

        delete_button = tk.Button(
            edit_delete_frame,
            text="Delete",
            command=lambda: delete_box(new_box_frame, establishment["estab_id"]),
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#B46617",
            bd=0,
            activebackground="#FFA500",
            activeforeground="white",
            cursor="hand2",
            width=7,
        )
        delete_button.pack(side="left", padx=3, pady=2)

        reviews_button = tk.Button(
            new_box_frame,
            text="Check Food Reviews",
            command=check_reviews,
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#B46617",
            bd=0,
            activebackground="#FFA500",
            activeforeground="white",
            cursor="hand2",
            width=20,
        )
        reviews_button.pack(side="top", padx=5, pady=2)

        check_items_button = tk.Button(
            new_box_frame,
            text="Check Food Items",
            command=lambda estab_id=establishment["estab_id"]: check_food_items(estab_id),
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#B46617",
            bd=0,
            activebackground="#FFA500",
            activeforeground="white",
            cursor="hand2",
            width=20,
        )
        check_items_button.pack(side="top", padx=5, pady=2)

    def check_food_items(establishment_id):
        owner_food_item(establishment_id)

    def delete_box(box_frame, estab_id):
        database = connect_to_db()
        if not database:
            return
        database_cursor = database.cursor()
        try:
            query = "SELECT item_id FROM food_item WHERE establishment_id=%s"
            database_cursor.execute(query, (estab_id,))
            item_ids = [row[0] for row in database_cursor.fetchall()]

            for item_id in item_ids:
                query = "DELETE FROM food_item_food_type WHERE item_id=%s"
                database_cursor.execute(query, (item_id,))

            query = "DELETE FROM food_item WHERE establishment_id=%s"
            database_cursor.execute(query, (estab_id,))

            query = "DELETE FROM food_establishment WHERE establishment_id=%s"
            database_cursor.execute(query, (estab_id,))

            database.commit()

            database_cursor.close()
            database.close()

            box_frame.destroy()
        except Exception as e:
            database.rollback()
            database_cursor.close()
            database.close()
            print("Error occurred:", e)


    def edit_item(box_frame, establishment):
        dialog = EditItemDialog(foodestabWindow, establishment)
        foodestabWindow.wait_window(dialog.top)
        if dialog.result:
            database = connect_to_db()
            if not database:
                return
            database_cursor = database.cursor()
            query = (
                "UPDATE food_establishment SET name = %s, location = %s, description = %s "
                "WHERE estab_id = %s"
            )
            values = (
                dialog.result["name"],
                dialog.result["location"],
                dialog.result["description"],
                establishment["estab_id"],
            )
            database_cursor.execute(query, values)
            database.commit()
            database_cursor.close()
            database.close()
            
            establishment.update(dialog.result)
            for widget in box_frame.winfo_children():
                widget.destroy()

            create_new_box(establishment)

    def check_reviews():
        print("Check Food Reviews button clicked")
        foodestabWindow.withdraw()
        estabReviews.establishmentReviews(foodestabWindow)
    
    def load_initial_data():
        clear_boxes()
        establishments_data = search_food_establishment("")
        for establishment in establishments_data:
            establishment_dict = {
                "estab_id": establishment[0],
                "location": establishment[1],
                "description": establishment[2],
                "average_rating": establishment[3],
                "name": establishment[4],
                "account_id": establishment[5],
            }
            create_new_box(establishment_dict)
    
    def clear_boxes():
        for widget in boxes_frame.grid_slaves():
            widget.destroy()

    def on_search():
        name = search_entry.get()
        clear_boxes()
        establishments_data = search_food_establishment(name)
        for establishment in establishments_data:
            establishment_dict = {
                "estab_id": establishment[0],
                "location": establishment[1],
                "description": establishment[2],
                "average_rating": establishment[3],
                "name": establishment[4],
                "account_id": establishment[5],
            }
            create_new_box(establishment_dict)
    
    foodestabWindow = tk.Tk()
    foodestabWindow.geometry("1100x650")
    foodestabWindow.configure(bg="white")
    foodestabWindow.title("My Food Establishments")

    search_frame = tk.Frame(foodestabWindow, bg="white")
    search_frame.pack(pady=20)

    search_label = tk.Label(search_frame, text="Search Food Establishment:", bg="white", foreground="#B46617", font=("Helvetica", 12, "bold"))
    search_label.pack(side="left")

    search_entry = ttk.Entry(search_frame, foreground="black", font=("Helvetica", 11))
    search_entry.pack(side="left")

    search_button = tk.Button(
        search_frame,
        text="Search",
        command=on_search,
        font=("Helvetica", 10, "bold"),
        fg="white",
        bg="#B46617",
        activebackground="#FFBA00",
        activeforeground="white"
    )
    search_button.pack(side="left", padx=10)

    add_item_button = tk.Button(
        search_frame,
        text="Add New Establishment",
        command=add_item,
        font=("Helvetica", 10, "bold"),
        fg="white",
        bg="#B46617",
        activebackground="#FFBA00",
        activeforeground="white"
    )
    add_item_button.pack(side="left", padx=10)

    canvas = tk.Canvas(foodestabWindow, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(foodestabWindow, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    boxes_frame = ttk.Frame(canvas, style="Custom.TFrame")

    canvas.create_window((0, 0), window=boxes_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    boxes_frame.bind("<Configure>", on_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    foodestabWindow.columnconfigure(0, weight=1)
    foodestabWindow.columnconfigure(1, weight=1)
    foodestabWindow.columnconfigure(2, weight=1)
    foodestabWindow.rowconfigure(2, weight=1)

    for i in range(3):
        foodestabWindow.columnconfigure(i, weight=1)
        foodestabWindow.rowconfigure(i + 2, weight=1)
    
    load_initial_data()
    foodestabWindow.mainloop()

owner_food_establishment(1)



