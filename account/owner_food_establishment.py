import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from owner_food_item import owner_food_item


def owner_food_establishment(account_id):
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

    def add_item():
        dialog = AddItemDialog(owner_food_establishment_window)
        owner_food_establishment_window.wait_window(dialog.top)
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
            dialog.result["establishment_id"] = database_cursor.lastrowid
            database_cursor.close()
            database.close()
            create_new_box(dialog.result)

    class AddItemDialog:
        def __init__(self, parent):
            self.top = tk.Toplevel(parent)
            self.top.title("Add New Item")
            self.top.geometry("300x250")
            self.result = None

            tk.Label(
                self.top,
                text="Establishment Name:",
                foreground="#B46617",
                font=("Helvetica", 12, "bold"),
            ).pack()
            self.estab_name_entry = ttk.Entry(
                self.top, foreground="black", font=("Helvetica", 11)
            )
            self.estab_name_entry.pack()

            tk.Label(
                self.top,
                text="Location:",
                foreground="#B46617",
                font=("Helvetica", 12, "bold"),
            ).pack()
            self.location_entry = ttk.Entry(
                self.top, foreground="black", font=("Helvetica", 11)
            )
            self.location_entry.pack()

            tk.Label(
                self.top,
                text="Description:",
                foreground="#B46617",
                font=("Helvetica", 12, "bold"),
            ).pack()
            self.description_text = tk.Text(
                self.top, foreground="black", font=("Helvetica", 11), height=5, wrap="word"
            )
            self.description_text.pack()

            tk.Button(
                self.top,
                text="Add",
                command=self.add,
                font=("Helvetica", 10, "bold"),
                fg="white",
                bg="#B46617",
                activebackground="#FFBA00",
                activeforeground="white",
            ).pack()

        def add(self):
            self.result = {
                "name": self.estab_name_entry.get(),
                "location": self.location_entry.get(),
                "description": self.description_text.get("1.0", tk.END).strip(),
            }
            self.top.destroy()

    class EditItemDialog:
        def __init__(self, parent, item):
            self.top = tk.Toplevel(parent)
            self.top.title("Edit Item")
            self.top.geometry("300x250")
            self.result = None

            tk.Label(
                self.top,
                text="Establishment Name:",
                foreground="#B46617",
                font=("Helvetica", 12, "bold"),
            ).pack()
            self.estab_name_entry = ttk.Entry(
                self.top, foreground="black", font=("Helvetica", 11)
            )
            self.estab_name_entry.pack()
            self.estab_name_entry.insert(0, item["name"])

            tk.Label(
                self.top,
                text="Location:",
                foreground="#B46617",
                font=("Helvetica", 12, "bold"),
            ).pack()
            self.location_entry = ttk.Entry(
                self.top, foreground="black", font=("Helvetica", 11)
            )
            self.location_entry.pack()
            self.location_entry.insert(0, item["location"])

            tk.Label(
                self.top,
                text="Description:",
                foreground="#B46617",
                font=("Helvetica", 12, "bold"),
            ).pack()
            self.description_text = tk.Text(
                self.top, foreground="black", font=("Helvetica", 11), height=5, wrap="word"
            )
            self.description_text.pack()
            self.description_text.insert(tk.END, item["description"])

            button = tk.Button(
                self.top,
                text="Update",
                command=self.update,
                font=("Helvetica", 10, "bold"),
                fg="white",
                bg="#B46617",
            )
            button.pack()

        def update(self):
            self.result = {
                "name": self.estab_name_entry.get(),
                "location": self.location_entry.get(),
                "description": self.description_text.get("1.0", tk.END).strip(),
            }
            self.top.destroy()


    def create_new_box(establishment):
        new_box_frame = tk.Frame(
            boxes_frame,
            bg="#FFFFFF",
            borderwidth=1,
            relief="solid",
            width=300,
            height=400,
        )
        new_box_frame.grid_propagate(False)
        new_box_frame.columnconfigure(0, weight=1)
        total_boxes = len(boxes_frame.grid_slaves())
        row_position = total_boxes // 3
        column_position = total_boxes % 3

        new_box_frame.grid(
            row=row_position, column=column_position, padx=20, pady=30, sticky="nsew"
        )

        item_name_label = tk.Label(
            new_box_frame,
            text=establishment["name"].strip(),
            bg="white",
            font=("Helvetica", 20, "bold"),
            foreground="#FFA500",
        )
        item_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        container = tk.Frame(new_box_frame, bg="#FFFFFF", bd=0)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        establishment_id_label = tk.Label(
            container,
            bg="#FFFFFF",
            text="Establishment ID",
            font=("Helvetica", 10, "bold"),
            fg="#B46617",
        )
        establishment_id_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        establishment_id_value_label = tk.Label(
            container,
            bg="#FFFFFF",
            text=establishment["establishment_id"],
            font=("Helvetica Neue Light", 10),
            fg="#B46617",
        )
        establishment_id_value_label.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        location_label = tk.Label(
            container,
            bg="#FFFFFF",
            text="Location",
            font=("Helvetica", 10, "bold"),
            fg="#B46617",
        )
        location_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        location_value_label = tk.Label(
            container,
            bg="#FFFFFF",
            text=establishment["location"],
            font=("Helvetica Neue Light", 10),
            fg="#B46617",
        )
        location_value_label.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        description_label = tk.Label(
            new_box_frame,
            bg="#FFFFFF",
            text="Description",
            font=("Helvetica", 10, "bold"),
            fg="#B46617",
        )
        description_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        description_text = tk.Text(
            new_box_frame,
            bg="#FFFFFF",
            font=("Helvetica Neue Light", 10),
            wrap="word",
            height=5,
            bd=0,
            fg="#B46617",
        )
        description_text.insert(tk.END, establishment["description"])
        description_text.configure(state="disabled")
        description_text.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        edit_button = tk.Button(
            new_box_frame,
            text="Edit",
            font=("Helvetica", 10, "bold"),
            command=lambda: edit_item(new_box_frame, establishment),
            fg="white",
            bg="#B46617",
            bd=0,
            activebackground="#FFA500",
            activeforeground="white",
            cursor="hand2",
            width=7,
        )
        edit_button.grid(row=4, column=0, columnspan=1, pady=5, sticky="s")

        delete_button = tk.Button(
            new_box_frame,
            text="Delete",
            command=lambda: delete_box(
                new_box_frame, establishment["establishment_id"]
            ),
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#B46617",
            bd=0,
            activebackground="#FFA500",
            activeforeground="white",
            cursor="hand2",
            width=7,
        )
        delete_button.grid(row=5, column=0, columnspan=1, pady=5, sticky="s")

        check_items_button = tk.Button(
            new_box_frame,
            text="Check Food Items",
            command=lambda establishment_id=establishment[
                "establishment_id"
            ]: check_food_items(establishment_id),
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#B46617",
            bd=0,
            activebackground="#FFA500",
            activeforeground="white",
            cursor="hand2",
            width=20,
        )
        check_items_button.grid(row=6, column=0, columnspan=1, pady=5, sticky="s")

        if total_boxes % 3 == 2:
            owner_food_establishment_window.grid_rowconfigure(
                row_position + 1, weight=1
            )
        
    def check_food_items(establishment_id):
        owner_food_item(establishment_id)

    def delete_box(box_frame, establishment_id):
        database = connect_to_db()
        if not database:
            return
        database_cursor = database.cursor()
        try:
            query = "SELECT item_id FROM food_item WHERE establishment_id=%s"
            database_cursor.execute(query, (establishment_id,))
            item_ids = [row[0] for row in database_cursor.fetchall()]

            for item_id in item_ids:
                query = "DELETE FROM food_item_food_type WHERE item_id=%s"
                database_cursor.execute(query, (item_id,))

            query = "DELETE FROM food_item WHERE establishment_id=%s"
            database_cursor.execute(query, (establishment_id,))

            query = "DELETE FROM food_establishment WHERE establishment_id=%s"
            database_cursor.execute(query, (establishment_id,))

            database.commit()

            database_cursor.close()
            database.close()

            on_search()
        except Exception as e:
            database.rollback()
            database_cursor.close()
            database.close()
            print("Error occurred:", e)

    def edit_item(box_frame, establishment):
        dialog = EditItemDialog(owner_food_establishment_window, establishment)
        owner_food_establishment_window.wait_window(dialog.top)
        if dialog.result:
            database = connect_to_db()
            if not database:
                return
            database_cursor = database.cursor()
            query = (
                "UPDATE food_establishment SET name = %s, location = %s, description = %s "
                "WHERE establishment_id = %s"
            )
            values = (
                dialog.result["name"],
                dialog.result["location"],
                dialog.result["description"],
                establishment["establishment_id"],
            )
            database_cursor.execute(query, values)
            database.commit()
            database_cursor.close()
            database.close()

            establishment.update(dialog.result)
            on_search()

    def load_initial_data(name=""):
        clear_boxes()
        establishments_data = search_food_establishment(name)
        for establishment in establishments_data:
            establishment_dict = {
                "establishment_id": establishment[0],
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
        load_initial_data(name)

    owner_food_establishment_window = tk.Tk()
    owner_food_establishment_window.geometry("1100x650")
    owner_food_establishment_window.title("My Food Establishments")
    owner_food_establishment_window.resizable(False, False)
    owner_food_establishment_window.configure(bg="white")

    page_title = tk.Label(
        owner_food_establishment_window,
        text="MY FOOD ESTABLISHMENT",
        font=("Helvetica", 20, "bold"),
        bg="white",
        fg="#FFBA00",
        anchor="n",
    )
    page_title.grid(row=0, column=0, columnspan=3, sticky="new", pady=10)

    search_frame = tk.Frame(owner_food_establishment_window, bg="#FFFFFF")
    search_frame.grid(row=1, column=1, pady=10, padx=(180, 20), sticky="ew")

    search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=50)
    search_entry.pack(side=tk.LEFT, padx=30)

    search_button = tk.Button(
        search_frame,
        text="Search",
        command=on_search,
        font=("Helvetica", 10, "bold"),
        fg="white",
        bg="#B46617",
        activebackground="#FFBA00",
        activeforeground="white",
        bd=0,
    )
    search_button.pack(side=tk.LEFT, padx=10)

    add_item_button = tk.Button(
        search_frame,
        text="Add New Establishment",
        command=add_item,
        font=("Helvetica", 10, "bold"),
        fg="white",
        bg="#B46617",
        activebackground="#FFBA00",
        activeforeground="white",
        bd=0,
    )
    add_item_button.pack(side="left", padx=10)

    canvas = tk.Canvas(owner_food_establishment_window, bg="#FFFFFF")
    scroll_y = tk.Scrollbar(
        owner_food_establishment_window, orient="vertical", command=canvas.yview
    )
    scroll_frame = tk.Frame(canvas, bg="#FFFFFF")

    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    scroll_y.grid(row=2, column=3, sticky="ns")
    canvas.grid(row=2, column=0, columnspan=3, padx=(30, 20), sticky="nsew")

    boxes_frame = tk.Frame(scroll_frame, bg="#FFFFFF")
    boxes_frame.grid(row=0, column=0, sticky="nsew")

    owner_food_establishment_window.columnconfigure(0, weight=1)
    owner_food_establishment_window.columnconfigure(1, weight=1)
    owner_food_establishment_window.columnconfigure(2, weight=1)
    owner_food_establishment_window.rowconfigure(2, weight=1)

    load_initial_data()
    owner_food_establishment_window.mainloop()
