import tkinter as tk
from tkinter import ttk
import Customer_EstabReviews

establishments_data = [
    {"name": "Restaurant A", "estab_id": "001", "location": "City Center", "description": "A cozy restaurant serving Italian cuisine."},
    {"name": "Cafe B", "estab_id": "002", "location": "Downtown", "description": "A trendy cafe offering specialty coffee and pastries."},
    {"name": "Bakery C", "estab_id": "003", "location": "Suburb", "description": "A family-owned bakery famous for its freshly baked bread and cakes."},
    {"name": "Bar D", "estab_id": "004", "location": "Waterfront", "description": "A lively bar with a wide selection of cocktails and live music."},
    {"name": "Pizzeria E", "estab_id": "005", "location": "Old Town", "description": "An authentic pizzeria known for its wood-fired pizzas."},
]

class AddItemDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Add New Item")
        self.top.geometry("300x200")
        self.result = None

        tk.Label(self.top, text="Establishment ID:").pack()
        self.estab_id_entry = ttk.Entry(self.top)
        self.estab_id_entry.pack()

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
            "estab_id": self.estab_id_entry.get(),
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

        tk.Label(self.top, text="Establishment ID:").pack()
        self.estab_id_entry = ttk.Entry(self.top)
        self.estab_id_entry.pack()
        self.estab_id_entry.insert(0, item["estab_id"])

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
            "estab_id": self.estab_id_entry.get(),
            "name": self.estab_name_entry.get(),
            "location": self.location_entry.get(),
            "description": self.description_entry.get(),
        }
        self.top.destroy()

def create_new_box(establishment):
    new_box_frame = ttk.Frame(foodestabWindow, borderwidth=1, relief="solid")
    total_boxes = len(foodestabWindow.grid_slaves()) - 1
    row_position = total_boxes // 3 + 1
    column_position = total_boxes % 3

    new_box_frame.grid(row=row_position, column=column_position, padx=20, pady=30, sticky="nsew")

    item_name_label = tk.Label(new_box_frame, text=establishment["name"])
    item_name_label.pack(expand=True)

    details_label = tk.Label(new_box_frame, text=f"ID: {establishment['estab_id']}\nLocation: {establishment['location']}\nDescription: {establishment['description']}", width=40)
    details_label.pack(expand=True)

    reviews_button = ttk.Button(new_box_frame, text="Check Reviews", command=check_reviews)
    reviews_button.pack(side="left", padx=5)

def delete_box(box_frame):
    box_frame.destroy()

def edit_item(box_frame, establishment):
    dialog = EditItemDialog(foodestabWindow, establishment)
    foodestabWindow.wait_window(dialog.top)
    if dialog.result:
        establishment.update(dialog.result)
        for widget in box_frame.winfo_children():
            widget.destroy()

        name_label = tk.Label(box_frame, text=establishment["name"], width=40)
        name_label.pack(expand=True)

        details_label = tk.Label(box_frame, text=f"ID: {establishment['estab_id']}\nLocation: {establishment['location']}\nDescription: {establishment['description']}", width=40)
        details_label.pack(expand=True)

        reviews_button = ttk.Button(box_frame, text="Check Food Reviews", command=check_reviews)
        reviews_button.pack(side="left", padx=5)

def check_reviews():
    print("Check Food Reviews button clicked")
    foodestabWindow.withdraw()
    Customer_EstabReviews.establishmentReviews(foodestabWindow)

foodestabWindow = tk.Tk()
foodestabWindow.geometry("1100x650")
foodestabWindow.title("Food Establishment Customer Account")
foodestabWindow.resizable(False, False)

foodestabWindow.configure(bg="#D3D3D3")

label1 = tk.Label(foodestabWindow, text="Food Establishment Customer Account", font=('Arial', 20, 'bold'), bg="white", fg="#FFBA00", anchor="nw")
label1.grid(row=0, column=0, columnspan=3, sticky="new")

foodestabWindow.columnconfigure(0, weight=1)
foodestabWindow.columnconfigure(1, weight=1)
foodestabWindow.rowconfigure(0, weight=1)

for i in range(3):
    foodestabWindow.columnconfigure(i, weight=1)
    foodestabWindow.rowconfigure(i + 1, weight=1)

for row in range(1):
    for col in range(3):
        box_index = row * 3 + col
        if box_index < len(establishments_data):
            establishment = establishments_data[box_index]
            create_new_box(establishment)

foodestabWindow.mainloop()
