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
                password="chancekababy2021",
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

            tk.Label(self.top, text="Establishment Name:").pack()
            self.estab_name_entry = ttk.Entry(self.top)
            self.estab_name_entry.pack()

            tk.Label(self.top, text="Location:").pack()
            self.location_entry = ttk.Entry(self.top)
            self.location_entry.pack()

            tk.Label(self.top, text="Description:").pack()
            self.description_entry = ttk.Entry(self.top)
            self.description_entry.pack()

            ttk.Button(self.top, text="Add", command=self.add).pack()

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

            tk.Label(self.top, text="Establishment Name:").pack()
            self.estab_name_entry = ttk.Entry(self.top)
            self.estab_name_entry.pack()
            self.estab_name_entry.insert(0, item["name"])

            tk.Label(self.top, text="Location:").pack()
            self.location_entry = ttk.Entry(self.top)
            self.location_entry.pack()
            self.location_entry.insert(0, item["location"])

            tk.Label(self.top, text="Description:").pack()
            self.description_entry = ttk.Entry(self.top)
            self.description_entry.pack()
            self.description_entry.insert(0, item["description"])

            ttk.Button(self.top, text="Update", command=self.update).pack()

        def update(self):
            self.result = {
                "name": self.estab_name_entry.get(),
                "location": self.location_entry.get(),
                "description": self.description_entry.get(),
            }
            self.top.destroy()

    def create_new_box(establishment):
        new_box_frame = ttk.Frame(foodestabWindow, borderwidth=1, relief="solid")
        total_boxes = len(foodestabWindow.grid_slaves()) - 2
        row_position = total_boxes // 3 + 2
        column_position = total_boxes % 3

        new_box_frame.grid(
            row=row_position, column=column_position, padx=20, pady=30, sticky="nsew"
        )

        item_name_label = tk.Label(new_box_frame, text=establishment["name"])
        item_name_label.pack(expand=True)

        details_label = tk.Label(
            new_box_frame,
            text=f"ID: {establishment['estab_id']}\nLocation: {establishment['location']}\nDescription: {establishment['description']}",
            width=40,
        )
        details_label.pack(expand=True)

        edit_button = ttk.Button(
            new_box_frame,
            text="Edit",
            command=lambda: edit_item(new_box_frame, establishment),
        )
        edit_button.pack(side="left", padx=5)

        delete_button = ttk.Button(
            new_box_frame,
            text="Delete",
            command=lambda: delete_box(new_box_frame, establishment["estab_id"]),
        )
        delete_button.pack(side="left", padx=5)

        reviews_button = ttk.Button(
            new_box_frame, text="Check Food Reviews", command=check_reviews
        )
        reviews_button.pack(side="left", padx=5)

        check_items_button = ttk.Button(
            new_box_frame,
            text="Check Food Items",
            command=lambda estab_id=establishment["estab_id"]: check_food_items(
                estab_id
            ),
        )
        check_items_button.pack(side="left", padx=5)

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
                "UPDATE food_establishment SET name=%s, location=%s, description=%s "
                "WHERE establishment_id=%s"
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

            name_label = tk.Label(box_frame, text=establishment["name"], width=40)
            name_label.pack(expand=True)

            details_label = tk.Label(
                box_frame,
                text=f"ID: {establishment['estab_id']}\nLocation: {establishment['location']}\nDescription: {establishment['description']}",
                width=40,
            )
            details_label.pack(expand=True)

            edit_button = ttk.Button(
                box_frame,
                text="Edit",
                command=lambda: edit_item(box_frame, establishment),
            )
            edit_button.pack(side="left", padx=5)

            delete_button = ttk.Button(
                box_frame,
                text="Delete",
                command=lambda: delete_box(box_frame, establishment["estab_id"]),
            )
            delete_button.pack(side="left", padx=5)

            reviews_button = ttk.Button(
                box_frame, text="Check Food Reviews", command=check_reviews
            )
            reviews_button.pack(side="left", padx=5)

            check_items_button = ttk.Button(
                box_frame,
                text="Check Food Items",
                command=lambda estab_id=establishment["estab_id"]: check_food_items(
                    estab_id
                ),
            )
            check_items_button.pack(side="left", padx=5)

    def check_reviews():
        print(
            "Check Food Reviews button clicked",
        )
        foodestabWindow.withdraw()
        estabReviews.establishmentReviews(foodestabWindow)

    def load_initial_data(name=""):
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

    def clear_boxes():
        for widget in foodestabWindow.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.destroy()

    def on_search():
        name = search_entry.get()
        load_initial_data(name)

    foodestabWindow = tk.Tk()
    foodestabWindow.geometry("1100x650")
    foodestabWindow.title("Food Establishment Owner Account")
    foodestabWindow.resizable(False, False)
    foodestabWindow.configure(bg="#D3D3D3")

    label1 = tk.Label(
        foodestabWindow,
        text="Food Establishment Owner Account",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#FFBA00",
        anchor="nw",
    )
    label1.grid(row=0, column=0, columnspan=3, sticky="new")

    # Search bar
    search_frame = tk.Frame(foodestabWindow, bg="#D3D3D3")
    search_frame.grid(row=1, column=0, columnspan=3, pady=10)

    tk.Label(
        search_frame, text="Search Establishments:", font=("Arial", 14), bg="#D3D3D3"
    ).pack(side=tk.LEFT, padx=10)
    search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
    search_entry.pack(side=tk.LEFT, padx=10)
    search_btn = tk.Button(
        search_frame, text="Search", font=("Arial", 14), command=on_search
    )
    search_btn.pack(side=tk.LEFT, padx=10)

    add_button = ttk.Button(foodestabWindow, text="Add", command=add_item)
    add_button.grid(row=0, column=1, pady=(20, 10))

    foodestabWindow.columnconfigure(0, weight=1)
    foodestabWindow.columnconfigure(1, weight=1)
    foodestabWindow.rowconfigure(0, weight=1)

    for i in range(3):
        foodestabWindow.columnconfigure(i, weight=1)
        foodestabWindow.rowconfigure(i + 2, weight=1)

    load_initial_data()
    foodestabWindow.mainloop()


owner_food_establishment(1)
