import tkinter as tk
from tkinter import ttk
import Customer_FoodItems

reviews = [
    {"review_id": "001", "reviewer_name": "John Doe", "rating": 5, "review_text": "Amazing food and great service!", "establishment": "Restaurant A"},
    {"review_id": "002", "reviewer_name": "Jane Smith", "rating": 4, "review_text": "Good coffee but a bit pricey.", "establishment": "Cafe B"},
    {"review_id": "003", "reviewer_name": "Emily Davis", "rating": 5, "review_text": "Best chocolate cake I've ever had!", "establishment": "Bakery C"},
    {"review_id": "004", "reviewer_name": "Michael Brown", "rating": 3, "review_text": "Nice atmosphere, but the drinks were average.", "establishment": "Bar D"},
]

def establishmentReviews(parent):

    def add_review():
        dialog = AddReviewDialog(estabReviews)
        estabReviews.wait_window(dialog.top)
        if dialog.result:
            reviews.append(dialog.result)
            create_new_box(dialog.result)

    def view_food_items():
    # Implement functionality to view food items
        pass

    class AddReviewDialog:
        def __init__(self, parent):
            self.top = tk.Toplevel(parent)
            self.top.title("Add New Review")
            self.top.geometry("300x300")
            self.result = None

            tk.Label(self.top, text="Review ID:").pack()
            self.review_id_entry = ttk.Entry(self.top)
            self.review_id_entry.pack()

            tk.Label(self.top, text="Reviewer Name:").pack()
            self.reviewer_name_entry = ttk.Entry(self.top)
            self.reviewer_name_entry.pack()

            tk.Label(self.top, text="Rating (1-5):").pack()
            self.rating_entry = ttk.Entry(self.top)
            self.rating_entry.pack()

            tk.Label(self.top, text="Review Text:").pack()
            self.review_text_entry = ttk.Entry(self.top)
            self.review_text_entry.pack()

            tk.Label(self.top, text="Establishment:").pack()
            self.establishment_entry = ttk.Entry(self.top)
            self.establishment_entry.pack()

            ttk.Button(self.top, text="Add", command=self.add).pack()

        def add(self):
            self.result = {
                "review_id": self.review_id_entry.get(),
                "reviewer_name": self.reviewer_name_entry.get(),
                "rating": int(self.rating_entry.get()),
                "review_text": self.review_text_entry.get(),
                "establishment": self.establishment_entry.get(),
            }
            self.top.destroy()

    class EditReviewDialog:
        def __init__(self, parent, review):
            self.top = tk.Toplevel(parent)
            self.top.title("Edit Review")
            self.top.geometry("300x300")
            self.result = None
            self.review = review

            tk.Label(self.top, text="Review ID:").pack()
            self.review_id_entry = ttk.Entry(self.top)
            self.review_id_entry.pack()
            self.review_id_entry.insert(0, review["review_id"])

            tk.Label(self.top, text="Reviewer Name:").pack()
            self.reviewer_name_entry = ttk.Entry(self.top)
            self.reviewer_name_entry.pack()
            self.reviewer_name_entry.insert(0, review["reviewer_name"])

            tk.Label(self.top, text="Rating (1-5):").pack()
            self.rating_entry = ttk.Entry(self.top)
            self.rating_entry.pack()
            self.rating_entry.insert(0, review["rating"])

            tk.Label(self.top, text="Review Text:").pack()
            self.review_text_entry = ttk.Entry(self.top)
            self.review_text_entry.pack()
            self.review_text_entry.insert(0, review["review_text"])

            tk.Label(self.top, text="Establishment:").pack()
            self.establishment_entry = ttk.Entry(self.top)
            self.establishment_entry.pack()
            self.establishment_entry.insert(0, review["establishment"])

            ttk.Button(self.top, text="Update", command=self.update).pack()

        def update(self):
            self.result = {
                "review_id": self.review_id_entry.get(),
                "reviewer_name": self.reviewer_name_entry.get(),
                "rating": int(self.rating_entry.get()),
                "review_text": self.review_text_entry.get(),
                "establishment": self.establishment_entry.get(),
            }
            self.top.destroy()

    def create_new_box(review):
        new_box_frame = ttk.Frame(estabReviews, borderwidth=1, relief="solid")
        total_boxes = len(estabReviews.grid_slaves()) - 1
        row_position = total_boxes // 3 + 1
        column_position = total_boxes % 3

        new_box_frame.grid(row=row_position, column=column_position, padx=20, pady=30, sticky="nsew")

        reviewer_name_label = tk.Label(new_box_frame, text=review["reviewer_name"])
        reviewer_name_label.pack(expand=True)

        details_label = tk.Label(new_box_frame, text=f"ID: {review['review_id']}\nRating: {review['rating']}\nReview: {review['review_text']}\nEstablishment: {review['establishment']}")
        details_label.pack(expand=True)

        edit_button = ttk.Button(new_box_frame, text="Edit", command=lambda: edit_review(new_box_frame, review))
        edit_button.pack(side="left", padx=5)

        delete_box_button = ttk.Button(new_box_frame, text="Delete", command=lambda: delete_box(new_box_frame))
        delete_box_button.pack(side="left", padx=5)

        if total_boxes % 3 == 2:
            estabReviews.grid_rowconfigure(row_position + 1, weight=1)

    def delete_box(box_frame):
        box_frame.destroy()

    def edit_review(box_frame, review):
        dialog = EditReviewDialog(estabReviews, review)
        estabReviews.wait_window(dialog.top)
        if dialog.result:
            review.update(dialog.result)
            for widget in box_frame.winfo_children():
                widget.destroy()

            reviewer_name_label = tk.Label(box_frame, text=review["reviewer_name"])
            reviewer_name_label.pack(expand=True)

            details_label = tk.Label(box_frame, text=f"ID: {review['review_id']}\nRating: {review['rating']}\nReview: {review['review_text']}\nEstablishment: {review['establishment']}")
            details_label.pack(expand=True)

            edit_button = ttk.Button(box_frame, text="Edit", command=lambda: edit_review(box_frame, review))
            edit_button.pack(side="left", padx=5)

            delete_box_button = ttk.Button(box_frame, text="Delete", command=lambda: delete_box(box_frame))
            delete_box_button.pack(side="left", padx=5)

    def go_back():
        parent.deiconify()
        estabReviews.destroy()

    def view_food_items():
        print("Food Items button clicked")
        estabReviews.withdraw()
        Customer_FoodItems.FoodReviews(estabReviews)

    estabReviews = tk.Tk()
    estabReviews.geometry("1100x650")
    estabReviews.title("Food Establishment Reviews")
    estabReviews.resizable(False, False)

    estabReviews.configure(bg="#D3D3D3")

    label1 = tk.Label(estabReviews, text="Food Establishment Reviews", font=('Arial', 20, 'bold'), bg="white", fg="#FFBA00", anchor="w")
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
            if box_index < len(reviews):
                review = reviews[box_index]
                create_new_box(review)

    add_button = ttk.Button(estabReviews, text="Add", command=add_review)
    add_button.grid(row=0, column=1, pady=(20, 10))

    view_food_items_button = ttk.Button(estabReviews, text="View Food Items", command=view_food_items)
    view_food_items_button.grid(row=0, column=2, pady=(20, 10))

    back_button = ttk.Button(estabReviews, text="Back", command=go_back)
    back_button.grid(row=0, column=0, pady=(20, 10))

    estabReviews.mainloop()