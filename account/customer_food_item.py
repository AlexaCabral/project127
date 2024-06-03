import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import customer_food_item_review


def customer_food_item(parent, account_id, establishment_id):
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

    def search_food_item(name):
        database = connect_to_db()
        if not database:
            return []

        database_cursor = database.cursor()
        query = f"SELECT item_id, name, price, description FROM food_item WHERE establishment_id={establishment_id} AND name LIKE '%{name}%'"
        database_cursor.execute(query)
        results = database_cursor.fetchall()
        database_cursor.close()
        database.close()
        return results

    def create_new_box(food_item):
        new_box_frame = tk.Frame(
            boxes_frame,
            bg="#FFFFFF",
            borderwidth=1,
            relief="solid",
            width=300,
            height=300,
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
            bg="#FFFFFF",
            text=food_item["name"],
            font=("Helvetica", 12, "bold"),
            fg="#FFBA00",
        )
        item_name_label.grid(row=0, column=0, pady=5, sticky="ew")

        container = tk.Frame(new_box_frame, bg="#FFFFFF", bd=0)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        item_id_label = tk.Label(
            container,
            bg="#FFFFFF",
            text="Item ID",
            font=("Helvetica", 10, "bold"),
            fg="#B46617",
        )
        item_id_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        item_id_value_label = tk.Label(
            container,
            bg="#FFFFFF",
            text=food_item["item_id"],
            font=("Helvetica Neue Light", 10),
            fg="#B46617",
        )
        item_id_value_label.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        price_label = tk.Label(
            container,
            bg="#FFFFFF",
            text="Price",
            font=("Helvetica", 10, "bold"),
            fg="#B46617",
        )
        price_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        price_value_label = tk.Label(
            container,
            bg="#FFFFFF",
            text=food_item["price"],
            font=("Helvetica Neue Light", 10),
            fg="#B46617",
        )
        price_value_label.grid(row=1, column=1, sticky="e", padx=5, pady=5)

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
        description_text.insert(tk.END, food_item["description"])
        description_text.configure(state="disabled")
        description_text.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        reviews_button = tk.Button(
            new_box_frame,
            text="Check Reviews",
            font=("Helvetica", 10),
            command=lambda item_id=food_item["item_id"]: check_food_item_reviews(
                item_id
            ),
            bg="#B46617",
            fg="white",
            bd=0,
        )
        reviews_button.grid(row=4, column=0, columnspan=1, pady=5, sticky="s")

        if total_boxes % 3 == 2:
            customer_food_item_window.grid_rowconfigure(row_position + 1, weight=1)

    def go_back():
        parent.deiconify()
        customer_food_item_window.destroy()

    def check_food_item_reviews(item_id):
        print("Check Food Reviews button clicked")
        customer_food_item_window.withdraw()
        customer_food_item_review.customer_food_item_review(
            customer_food_item_window, item_id, establishment_id, account_id
        )

    def clear_boxes():
        for widget in boxes_frame.grid_slaves():
            widget.destroy()

    def load_initial_data(name=""):
        clear_boxes()
        food_items = search_food_item(name)
        for food_item in food_items:
            food_item_data = {
                "item_id": food_item[0],
                "name": food_item[1],
                "price": food_item[2],
                "description": food_item[3],
            }
            create_new_box(food_item_data)

    def on_search():
        name = search_entry.get()
        load_initial_data(name)

    customer_food_item_window = tk.Tk()
    customer_food_item_window.geometry("1100x650")
    customer_food_item_window.title("Food Establishment Food Item List")
    customer_food_item_window.resizable(False, False)
    customer_food_item_window.configure(bg="#FFFFFF")

    label1 = tk.Label(
        customer_food_item_window,
        text="FOOD ITEM",
        font=("Helvetica", 20, "bold"),
        bg="white",
        fg="#FFBA00",
        anchor="n",
    )
    label1.grid(row=0, column=0, columnspan=3, sticky="new", pady=10)

    search_frame = tk.Frame(customer_food_item_window, bg="#FFFFFF")
    search_frame.grid(row=1, column=1, pady=10, padx=(180, 20), sticky="ew")

    search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=50)
    search_entry.pack(side=tk.LEFT, padx=30)

    search_btn = tk.Button(
        search_frame,
        text="Search",
        font=("Helvetica", 12, "bold"),
        command=on_search,
        bg="#B46617",
        fg="white",
        bd=0,
    )
    search_btn.pack(side=tk.LEFT, padx=10)

    canvas = tk.Canvas(customer_food_item_window, bg="#FFFFFF")
    scroll_y = tk.Scrollbar(
        customer_food_item_window, orient="vertical", command=canvas.yview
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

    customer_food_item_window.columnconfigure(0, weight=1)
    customer_food_item_window.columnconfigure(1, weight=1)
    customer_food_item_window.columnconfigure(2, weight=1)
    customer_food_item_window.rowconfigure(5, weight=1)

    back_button = tk.Button(
        customer_food_item_window, 
        text="Back", 
        command=go_back,
        font=("Arial", 12, "bold"),
        bg="#B46617",
        fg="white",
        bd=0
    )
    back_button.grid(row=5, column=0, pady=20)

    load_initial_data()
    customer_food_item_window.mainloop()
