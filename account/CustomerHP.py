import tkinter as tk
from tkinter import ttk

# Sample data for demonstration
establishments_data = [
    {"name": "Restaurant A", "estab_id": "001", "location": "City Center", "description": "A cozy restaurant serving Italian cuisine."},
    {"name": "Cafe B", "estab_id": "002", "location": "Downtown", "description": "A trendy cafe offering specialty coffee and pastries."},
    {"name": "Bakery C", "estab_id": "003", "location": "Suburb", "description": "A family-owned bakery famous for its freshly baked bread and cakes."},
    {"name": "Bar D", "estab_id": "004", "location": "Waterfront", "description": "A lively bar with a wide selection of cocktails and live music."},
    {"name": "Pizzeria E", "estab_id": "005", "location": "Old Town", "description": "An authentic pizzeria known for its wood-fired pizzas."},
]

food_items = [
    {"item_id": "001", "item_name": "Spaghetti Carbonara", "food_type": "Pasta", "price": 12.99, "description": "Classic spaghetti dish with creamy carbonara sauce."},
    {"item_id": "002", "item_name": "Espresso", "food_type": "Coffee", "price": 3.49, "description": "Strong black coffee brewed to perfection."},
    {"item_id": "003", "item_name": "Chocolate Cake", "food_type": "Dessert", "price": 6.99, "description": "Decadent chocolate cake topped with chocolate ganache."},
    {"item_id": "004", "item_name": "Mojito", "food_type": "Cocktail", "price": 8.99, "description": "Refreshing cocktail made with rum, mint, lime, and soda water."},
]

class AddReviewDialog:
    def __init__(self, parent, food_item):
        self.top = tk.Toplevel(parent)
        self.top.title("Add Review")
        self.top.geometry("300x200")
        self.result = None
        self.food_item = food_item

        tk.Label(self.top, text=f"Review for {food_item['item_name']}:").pack()
        self.review_entry = ttk.Entry(self.top)
        self.review_entry.pack()

        ttk.Button(self.top, text="Add", command=self.add_review).pack()

    def add_review(self):
        review_text = self.review_entry.get()
        if review_text.strip() == "":
            messagebox.showwarning("Error", "Please enter a review.")
        else:
            self.result = {
                "food_item": self.food_item,
                "review": review_text,
            }
            self.top.destroy()

def add_review_dialog(food_item):
    dialog = AddReviewDialog(root, food_item)
    root.wait_window(dialog.top)
    if dialog.result:
        review = dialog.result["review"]
        print(f"Review added for {food_item['item_name']}: {review}")

class AddRestaurantReviewDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Add Restaurant Review")
        self.top.geometry("300x200")
        self.result = None

        tk.Label(self.top, text="Review for the Restaurant:").pack()
        self.review_entry = ttk.Entry(self.top)
        self.review_entry.pack()

        ttk.Button(self.top, text="Add", command=self.add_review).pack()

    def add_review(self):
        review_text = self.review_entry.get()
        if review_text.strip() == "":
            messagebox.showwarning("Error", "Please enter a review.")
        else:
            self.result = {
                "review": review_text,
            }
            self.top.destroy()

def add_restaurant_review_dialog():
    dialog = AddRestaurantReviewDialog(root)
    root.wait_window(dialog.top)
    if dialog.result:
        review = dialog.result["review"]
        print(f"Review added for the restaurant: {review}")

def goto_next_page(establishment):
    for widget in root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack()

    back_button = tk.Button(root, text="Go Back", command=lambda: show_frame(main_frame))
    canvas.create_window(50, 50, anchor="nw", window=back_button)

    restaurant_name_label = tk.Label(root, text=f"Restaurant: {establishment['name']}", font=("Arial", 14, "bold"))
    canvas.create_window(50, 100, anchor="nw", window=restaurant_name_label)

    restaurant_review_button = tk.Button(root, text="Add Restaurant Review", command=add_restaurant_review_dialog)
    canvas.create_window(50, 150, anchor="nw", window=restaurant_review_button)

    x_offset = 100
    y_offset = 200
    box_width = 200
    box_height = 150
    gap = 20

    for food_item in food_items:
        food_box = tk.Frame(canvas, width=box_width, height=box_height, bd=2, relief="solid")
        canvas.create_window(x_offset, y_offset, anchor="nw", window=food_box)

        item_name_label = tk.Label(food_box, text=food_item["item_name"], font=("Arial", 12, "bold"))
        item_name_label.pack(pady=5)

        item_type_label = tk.Label(food_box, text=food_item["food_type"], font=("Arial", 10))
        item_type_label.pack()

        item_price_label = tk.Label(food_box, text="$" + str(food_item["price"]), font=("Arial", 10, "bold"))
        item_price_label.pack(pady=5)

        add_button = tk.Button(food_box, text="Add Review", command=lambda item=food_item: add_review_dialog(item))
        add_button.pack(pady=5)

        x_offset += box_width + gap
        if x_offset + box_width > window_width:
            x_offset = 100
            y_offset += box_height + gap

def add_establishment():
    global current_index
    if current_index < len(establishments_data):
        establishment = establishments_data[current_index]

        row = current_index // 3
        col = current_index % 3

        estab_frame = tk.Frame(main_frame, bd=2, relief="solid", padx=10, pady=10)
        estab_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        def on_box_click(event, establishment):
            goto_next_page(establishment)

        name_label = tk.Label(estab_frame, text=establishment["name"], font=("Arial", 12, "bold"))
        name_label.pack(anchor="w")

        name_label.bind("<Button-1>", lambda event, establishment=establishment: on_box_click(event, establishment))

        location_label = tk.Label(estab_frame, text=f"Location: {establishment['location']}", font=("Arial", 10))
        location_label.pack(anchor="w")

        description_label = tk.Label(estab_frame, text=establishment["description"], font=("Arial", 10), wraplength=250)
        description_label.pack(anchor="w")

        current_index += 1


def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title("Customer Homepage")
window_width = 1100
window_height = 650
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

x1, y1 = 10, 10
x2, y2 = window_width - 10, 50

canvas.create_rectangle(x1, y1, x2, y2, fill="#A49181", outline="")
margin = 20
text_x = x1 + margin
text_y = (y1 + y2) / 2
canvas.create_text(text_x, text_y, anchor="w", text="REVIEW127", font=("Arial", 14), fill="white")

space_between = 20
second_width = 500
second_height = 40
x3 = x1 + ((x2 - x1) - second_width) / 2
y3 = y2 + space_between
x4 = x3 + second_width
y4 = y3 + second_height

entry_width = 40
entry_x = x3 + 10
entry_y = y3 + 5
search_entry = tk.Entry(root, width=entry_width)
canvas.create_window(entry_x, entry_y, anchor="nw", window=search_entry)

button_width = 10
button_height = 25
button_x = x4 - button_width - 10
button_y = y3 + (second_height - button_height) / 2
search_button = tk.Button(root, text="Search", width=button_width)
canvas.create_window(button_x, button_y, anchor="nw", window=search_button)

add_button = tk.Button(root, text="Add Establishment", command=add_establishment)
canvas.create_window(window_width // 2 - 50, y4 + space_between, anchor="nw", window=add_button)

main_frame = tk.Frame(root)
main_frame.place(x=10, y=y4 + space_between + 50, width=window_width - 20, height=window_height - (y4 + space_between + 60))

current_index = 0

show_frame(main_frame)

root.mainloop()
