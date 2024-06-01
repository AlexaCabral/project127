import tkinter as tk
from tkinter import ttk

food_items = [
    {"item_id": "001", "item_name": "Spaghetti Carbonara", "food_type": "Pasta", "price": 12.99, "description": "Classic spaghetti dish with creamy carbonara sauce."},
    {"item_id": "002", "item_name": "Espresso", "food_type": "Coffee", "price": 3.49, "description": "Strong black coffee brewed to perfection."},
    {"item_id": "003", "item_name": "Chocolate Cake", "food_type": "Dessert", "price": 6.99, "description": "Decadent chocolate cake topped with chocolate ganache."},
    {"item_id": "004", "item_name": "Mojito", "food_type": "Cocktail", "price": 8.99, "description": "Refreshing cocktail made with rum, mint, lime, and soda water."},
]

def establishmentReviews(parent):

    def add_item():
        dialog = AddItemDialog(estabReviews)
        estabReviews.wait_window(dialog.top)
        if dialog.result:
            food_items.append(dialog.result)
            create_new_box(dialog.result)

    class AddItemDialog:
        def __init__(self, parent):
            self.top = tk.Toplevel(parent)
            self.top.title("Add New Item")
            self.top.geometry("300x200")
            self.result = None

            tk.Label(self.top, text="Item ID:").pack()
            self.item_id_entry = ttk.Entry(self.top)
            self.item_id_entry.pack()

            tk.Label(self.top, text="Item Name:").pack()
            self.item_name_entry = ttk.Entry(self.top)
            self.item_name_entry.pack()

            tk.Label(self.top, text="Price:").pack()
            self.price_entry = ttk.Entry(self.top)
            self.price_entry.pack()

            tk.Label(self.top, text="Food Type:").pack()
            self.food_type_entry = ttk.Entry(self.top)
            self.food_type_entry.pack()

            tk.Label(self.top, text="Description:").pack()
            self.description_entry = ttk.Entry(self.top)
            self.description_entry.pack()

            ttk.Button(self.top, text="Add", command=self.add).pack()

        def add(self):
            self.result = {
                "item_id": self.item_id_entry.get(),
                "item_name": self.item_name_entry.get(),
                "price": float(self.price_entry.get()),
                "food_type": self.food_type_entry.get(),
                "description": self.description_entry.get(),
            }
            self.top.destroy()

    class EditItemDialog:
        def __init__(self, parent, item):
            self.top = tk.Toplevel(parent)
            self.top.title("Edit Item")
            self.top.geometry("300x200")
            self.result = None
            self.item = item

            tk.Label(self.top, text="Item ID:").pack()
            self.item_id_entry = ttk.Entry(self.top)
            self.item_id_entry.pack()
            self.item_id_entry.insert(0, item["item_id"])

            tk.Label(self.top, text="Item Name:").pack()
            self.item_name_entry = ttk.Entry(self.top)
            self.item_name_entry.pack()
            self.item_name_entry.insert(0, item["item_name"])

            tk.Label(self.top, text="Price:").pack()
            self.price_entry = ttk.Entry(self.top)
            self.price_entry.pack()
            self.price_entry.insert(0, item["price"])

            tk.Label(self.top, text="Food Type:").pack()
            self.food_type_entry = ttk.Entry(self.top)
            self.food_type_entry.pack()
            self.food_type_entry.insert(0, item["food_type"])

            tk.Label(self.top, text="Description:").pack()
            self.description_entry = ttk.Entry(self.top)
            self.description_entry.pack()
            self.description_entry.insert(0, item["description"])

            ttk.Button(self.top, text="Update", command=self.update).pack()

        def update(self):
            self.result = {
                "item_id": self.item_id_entry.get(),
                "item_name": self.item_name_entry.get(),
                "price": float(self.price_entry.get()),
                "food_type": self.food_type_entry.get(),
                "description": self.description_entry.get(),
            }
            self.top.destroy()

    def create_new_box(foodItem):
        new_box_frame = ttk.Frame(estabReviews, borderwidth=1, relief="solid")
        total_boxes = len(estabReviews.grid_slaves()) - 1
        row_position = total_boxes // 3 + 1
        column_position = total_boxes % 3

        new_box_frame.grid(row=row_position, column=column_position, padx=20, pady=30, sticky="nsew")

        item_name_label = tk.Label(new_box_frame, text=foodItem["item_name"])
        item_name_label.pack(expand=True)

        details_label = tk.Label(new_box_frame, text=f"ID: {foodItem['item_id']}\nFood Type: {foodItem['food_type']}\nPrice: {foodItem['price']}\nDescription: {foodItem['description']}")
        details_label.pack(expand=True)

        edit_button = ttk.Button(new_box_frame, text="Edit", command=lambda: edit_item(new_box_frame, foodItem))
        edit_button.pack(side="left", padx=5)

        delete_box_button = ttk.Button(new_box_frame, text="Delete", command=lambda: delete_box(new_box_frame))
        delete_box_button.pack(side="left", padx=5)

        if total_boxes % 3 == 2:
            estabReviews.grid_rowconfigure(row_position + 1, weight=1)

    def delete_box(box_frame):
        box_frame.destroy()

    def edit_item(box_frame, foodItem):
        dialog = EditItemDialog(estabReviews, foodItem)
        estabReviews.wait_window(dialog.top)
        if dialog.result:
            foodItem.update(dialog.result)
            for widget in box_frame.winfo_children():
                widget.destroy()

            item_name_label = tk.Label(box_frame, text=foodItem["item_name"])
            item_name_label.pack(expand=True)

            details_label = tk.Label(box_frame, text=f"ID: {foodItem['item_id']}\nFood Type: {foodItem['food_type']}\nPrice: {foodItem['price']}\nDescription: {foodItem['description']}")
            details_label.pack(expand=True)

            edit_button = ttk.Button(box_frame, text="Edit", command=lambda: edit_item(box_frame, foodItem))
            edit_button.pack(side="left", padx=5)

            delete_box_button = ttk.Button(box_frame, text="Delete", command=lambda: delete_box(box_frame))
            delete_box_button.pack(side="left", padx=5)

    def go_back():
        parent.deiconify()
        estabReviews.destroy()

    estabReviews = tk.Tk()
    estabReviews.geometry("1100x650")
    estabReviews.title("Food Establishment Food Reviews")
    estabReviews.resizable(False, False)

    estabReviews.configure(bg="#D3D3D3")

    label1 = tk.Label(estabReviews, text="Food Establishment Food Reviews", font=('Arial', 20, 'bold'), bg="white", fg="#FFBA00", anchor="w")
    label1.grid(row=0, column=0, columnspan=3, sticky="new")

    estabReviews.columnconfigure(0, weight=1)
    estabReviews.columnconfigure(1, weight=1)
    estabReviews.rowconfigure(0, weight=1)

    for i in range(3):
        estabReviews.columnconfigure(i, weight=1)
        estabReviews.rowconfigure(i + 1, weight=1)

    for row in range(1):
        for col in range(3):
            box_index = row * 3 + col
            if box_index < len(food_items):
                foodItem = food_items[box_index]
                create_new_box(foodItem)

    add_button = ttk.Button(estabReviews, text="Add", command=add_item)
    add_button.grid(row=0, column=1, pady=(20, 10))

    back_button = ttk.Button(estabReviews, text="Back", command=go_back)
    back_button.grid(row=0, column=0, pady=(20, 10))

    estabReviews.mainloop()
