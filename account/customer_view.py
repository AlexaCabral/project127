import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import Customer_EstabReviews


def customer_food_establishment(account_id):
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

        reviews_button = ttk.Button(
            new_box_frame, text="Check Food Reviews", command=lambda estab_id=establishment['estab_id']: check_reviews(estab_id)
        )
        reviews_button.pack(side="left", padx=5)

    def check_reviews(estab_id):
        print("Check Food Reviews button clicked")
        foodestabWindow.withdraw()
        Customer_EstabReviews.establishmentReviews(foodestabWindow, estab_id)

    def clear_boxes():
        for widget in foodestabWindow.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.destroy()

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

    def on_search():
        name = search_entry.get()
        load_initial_data(name)

    foodestabWindow = tk.Tk()
    foodestabWindow.geometry("1100x650")
    foodestabWindow.title("Food Establishment Customer Account")
    foodestabWindow.resizable(False, False)
    foodestabWindow.configure(bg="#D3D3D3")

    label1 = tk.Label(
        foodestabWindow,
        text="Food Establishment Customer Account",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#FFBA00",
        anchor="nw",
    )
    label1.grid(row=0, column=0, columnspan=3, sticky="new")

    # Search bar
    search_frame = tk.Frame(foodestabWindow, bg="#D3D3D3")
    search_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=20, sticky="ew")

    tk.Label(
        search_frame, text="Search Establishments:", font=("Arial", 14), bg="#D3D3D3"
    ).pack(side=tk.LEFT, padx=10)

    search_entry = tk.Entry(search_frame, font=("Arial", 14), width=30)
    search_entry.pack(side=tk.LEFT, padx=10)

    search_btn = tk.Button(
        search_frame, text="Search", font=("Arial", 14), command=on_search
    )
    search_btn.pack(side=tk.LEFT, padx=10)

    foodestabWindow.columnconfigure(0, weight=1)
    foodestabWindow.columnconfigure(1, weight=1)
    foodestabWindow.columnconfigure(2, weight=1)

    load_initial_data()
    foodestabWindow.mainloop()


customer_food_establishment(1)
