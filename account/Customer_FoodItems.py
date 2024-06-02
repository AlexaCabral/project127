import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import Customer_FoodReviews

def FoodReviews(parent, account_id, establishment_id):

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

    def fetch_food_items():
        database = connect_to_db()
        if not database:
            return []

        database_cursor = database.cursor()
        query = f"SELECT item_id, name, price, description FROM food_item WHERE establishment_id={establishment_id}"
        print(query)
        database_cursor.execute(query)
        results = database_cursor.fetchall()
        database_cursor.close()
        database.close()
        return results

    def create_new_box(foodItem):
        new_box_frame = ttk.Frame(food_Reviews, borderwidth=1, relief="solid")
        total_boxes = len(food_Reviews.grid_slaves()) - 1
        row_position = total_boxes // 3 + 1
        column_position = total_boxes % 3

        new_box_frame.grid(row=row_position, column=column_position, padx=20, pady=30, sticky="nsew")

        item_name_label = tk.Label(new_box_frame, text=foodItem["name"])
        item_name_label.pack(expand=True)

        details_label = tk.Label(new_box_frame, text=f"ID: {foodItem['item_id']}\nPrice: {foodItem['price']}\nDescription: {foodItem['description']}")
        details_label.pack(expand=True)

        check_food_item_reviews_button = ttk.Button(new_box_frame, text="Check Food Item Reviews", command=lambda: check_food_item_reviews(foodItem["item_id"]))
        check_food_item_reviews_button.pack(side="left", padx=5)

        if total_boxes % 3 == 2:
            food_Reviews.grid_rowconfigure(row_position + 1, weight=1)

    def go_back():
        parent.deiconify()
        food_Reviews.destroy()

    def check_food_item_reviews(item_id):
        print("Check Food Reviews button clicked")
        food_Reviews.withdraw()
        Customer_FoodReviews.FoodItem_Reviews(food_Reviews, item_id, establishment_id, account_id)

    food_Reviews = tk.Tk()
    food_Reviews.geometry("1100x650")
    food_Reviews.title("Food Establishment Food Item List")
    food_Reviews.resizable(False, False)
    food_Reviews.configure(bg="#D3D3D3")

    label1 = tk.Label(food_Reviews, text="Food Establishment Food Item List", font=('Arial', 20, 'bold'), bg="white", fg="#FFBA00", anchor="w")
    label1.grid(row=0, column=0, columnspan=3, sticky="new")

    food_Reviews.columnconfigure(0, weight=1)
    food_Reviews.columnconfigure(1, weight=1)
    food_Reviews.rowconfigure(0, weight=1)

    for i in range(3):
        food_Reviews.columnconfigure(i, weight=1)
        food_Reviews.rowconfigure(i + 1, weight=1)

    food_items_data = fetch_food_items()
    for food_item in food_items_data:
        foodItem = {
            "item_id": food_item[0],
            "name": food_item[1],
            "price": food_item[2],
            "description": food_item[3]
        }
        create_new_box(foodItem)

    back_button = ttk.Button(food_Reviews, text="Back", command=go_back)
    back_button.grid(row=0, column=0, pady=(20, 10))

    food_Reviews.mainloop()
