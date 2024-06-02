import tkinter as tk
from tkinter import ttk
import Customer_FoodReviews


food_items = [
    {"item_id": "001", "item_name": "Spaghetti Carbonara", "food_type": "Pasta", "price": 12.99, "description": "Classic spaghetti dish with creamy carbonara sauce."},
    {"item_id": "002", "item_name": "Espresso", "food_type": "Coffee", "price": 3.49, "description": "Strong black coffee brewed to perfection."},
    {"item_id": "003", "item_name": "Chocolate Cake", "food_type": "Dessert", "price": 6.99, "description": "Decadent chocolate cake topped with chocolate ganache."},
    {"item_id": "004", "item_name": "Mojito", "food_type": "Cocktail", "price": 8.99, "description": "Refreshing cocktail made with rum, mint, lime, and soda water."},
]

def FoodReviews(parent):

    def create_new_box(foodItem):
        new_box_frame = ttk.Frame(food_Reviews, borderwidth=1, relief="solid")
        total_boxes = len(food_Reviews.grid_slaves()) - 1
        row_position = total_boxes // 3 + 1
        column_position = total_boxes % 3

        new_box_frame.grid(row=row_position, column=column_position, padx=20, pady=30, sticky="nsew")

        item_name_label = tk.Label(new_box_frame, text=foodItem["item_name"])
        item_name_label.pack(expand=True)

        details_label = tk.Label(new_box_frame, text=f"ID: {foodItem['item_id']}\nFood Type: {foodItem['food_type']}\nPrice: {foodItem['price']}\nDescription: {foodItem['description']}")
        details_label.pack(expand=True)

        check_food_item_reviews_button = ttk.Button(new_box_frame, text="Check Food Item Reviews", command=check_food_item_reviews)
        check_food_item_reviews_button.pack(side="left", padx=5)

        if total_boxes % 3 == 2:
            food_Reviews.grid_rowconfigure(row_position + 1, weight=1)

    def go_back():
        parent.deiconify()
        food_Reviews.destroy()
    
    def check_food_item_reviews():
        print("Check Food Reviews button clicked")
        food_Reviews.withdraw()
        Customer_FoodReviews.FoodItem_Reviews(food_Reviews)

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

    for row in range(1):
        for col in range(3):
            box_index = row * 3 + col
            if box_index < len(food_items):
                foodItem = food_items[box_index]
                create_new_box(foodItem)

    back_button = ttk.Button(food_Reviews, text="Back", command=go_back)
    back_button.grid(row=0, column=0, pady=(20, 10))

    food_Reviews.mainloop()
