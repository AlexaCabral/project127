import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import Customer_FoodItems


def FoodItem_Reviews(parent, item_id, establishment_id, account_id):
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

    def fetch_reviews(item_id):
        database = connect_to_db()
        if not database:
            return []

        database_cursor = database.cursor()
        query = f"SELECT review_id, rating, review_text FROM food_review WHERE item_id = {item_id} AND establishment_id = {establishment_id}"
        database_cursor.execute(query)
        results = database_cursor.fetchall()

        reviews = [
            {
                "review_id": r[0],
                "rating": r[1],
                "review_text": r[2],
            }
            for r in results
        ]

        database_cursor.close()
        database.close()
        return reviews

    def add_review_to_db(review):
        database = connect_to_db()
        if not database:
            return None

        database_cursor = database.cursor()
        query = "INSERT INTO food_review (rating, review_text, account_id, item_id, establishment_id) VALUES (%s, %s, %s, %s, %s)"
        database_cursor.execute(
            query,
            (
                review["rating"],
                review["review_text"],
                account_id,
                item_id,
                establishment_id,
            ),
        )
        database.commit()

        review_id = database_cursor.lastrowid
        database_cursor.close()
        database.close()
        return review_id

    def update_review_in_db(review):
        database = connect_to_db()
        if not database:
            return

        database_cursor = database.cursor()
        query = "UPDATE food_review SET rating = %s, review_text = %s WHERE review_id = %s"
        database_cursor.execute(
            query,
            (
                review["rating"],
                review["review_text"],
                review["review_id"]
            ),
        )
        database.commit()

        database_cursor.close()
        database.close()

    def delete_review_from_db(review_id):
        database = connect_to_db()
        if not database:
            return

        database_cursor = database.cursor()
        query = "DELETE FROM food_review WHERE review_id = %s"
        database_cursor.execute(query, (review_id,))
        database.commit()

        database_cursor.close()
        database.close()

    def add_review():
        dialog = AddReviewDialog(FoodItemReviews)
        FoodItemReviews.wait_window(dialog.top)
        if dialog.result:
            review_id = add_review_to_db(dialog.result)
            if review_id:
                dialog.result["review_id"] = review_id
                create_new_box(dialog.result)

    class AddReviewDialog:
        def __init__(self, parent):
            self.top = tk.Toplevel(parent)
            self.top.title("Add New Review")
            self.top.geometry("300x300")
            self.result = None

            tk.Label(self.top, text="Rating (1-5):").pack()
            self.rating_entry = ttk.Entry(self.top)
            self.rating_entry.pack()

            tk.Label(self.top, text="Review Text:").pack()
            self.review_text_entry = ttk.Entry(self.top)
            self.review_text_entry.pack()

            ttk.Button(self.top, text="Add", command=self.add).pack()

        def add(self):
            self.result = {
                "rating": int(self.rating_entry.get()),
                "review_text": self.review_text_entry.get(),
            }
            self.top.destroy()

    class EditReviewDialog:
        def __init__(self, parent, review):
            self.top = tk.Toplevel(parent)
            self.top.title("Edit Review")
            self.top.geometry("300x300")
            self.result = None
            self.review = review

            tk.Label(self.top, text="Rating (1-5):").pack()
            self.rating_entry = ttk.Entry(self.top)
            self.rating_entry.pack()
            self.rating_entry.insert(0, review["rating"])

            tk.Label(self.top, text="Review Text:").pack()
            self.review_text_entry = ttk.Entry(self.top)
            self.review_text_entry.pack()
            self.review_text_entry.insert(0, review["review_text"])

            ttk.Button(self.top, text="Update", command=self.update).pack()

        def update(self):
            self.result = {
                "review_id": self.review["review_id"],
                "rating": int(self.rating_entry.get()),
                "review_text": self.review_text_entry.get(),
            }
            self.top.destroy()

    def create_new_box(review):
        new_box_frame = ttk.Frame(FoodItemReviews, borderwidth=1, relief="solid")
        total_boxes = len(FoodItemReviews.grid_slaves()) - 1
        row_position = total_boxes // 3 + 1
        column_position = total_boxes % 3

        new_box_frame.grid(row=row_position, column=column_position, padx=20, pady=30, sticky="nsew")

        details_label = tk.Label(new_box_frame, text=f"ID: {review['review_id']}\nRating: {review['rating']}\nReview: {review['review_text']}")
        details_label.pack(expand=True)

        edit_button = ttk.Button(new_box_frame, text="Edit", command=lambda: edit_review(new_box_frame, review))
        edit_button.pack(side="left", padx=5)

        delete_box_button = ttk.Button(new_box_frame, text="Delete", command=lambda: delete_box(new_box_frame, review["review_id"]))
        delete_box_button.pack(side="left", padx=5)

        if total_boxes % 3 == 2:
            FoodItemReviews.grid_rowconfigure(row_position + 1, weight=1)

    def delete_box(box_frame, review_id):
        delete_review_from_db(review_id)
        box_frame.destroy()

    def edit_review(box_frame, review):
        dialog = EditReviewDialog(FoodItemReviews, review)
        FoodItemReviews.wait_window(dialog.top)
        if dialog.result:
            update_review_in_db(dialog.result)
            review.update(dialog.result)
            for widget in box_frame.winfo_children():
                widget.destroy()

            details_label = tk.Label(box_frame, text=f"ID: {review['review_id']}\nRating: {review['rating']}\nReview: {review['review_text']}")
            details_label.pack(expand=True)

            edit_button = ttk.Button(box_frame, text="Edit", command=lambda: edit_review(box_frame, review))
            edit_button.pack(side="left", padx=5)

            delete_box_button = ttk.Button(box_frame, text="Delete", command=lambda: delete_box(box_frame, review["review_id"]))
            delete_box_button.pack(side="left", padx=5)

    def go_back():
        parent.deiconify()
        FoodItemReviews.destroy()

    FoodItemReviews = tk.Tk()
    FoodItemReviews.geometry("1100x650")
    FoodItemReviews.title("Food Item Reviews")
    FoodItemReviews.resizable(False, False)
    FoodItemReviews.configure(bg="#D3D3D3")

    label1 = tk.Label(FoodItemReviews, text="Food Item Reviews", font=('Arial', 20, 'bold'), bg="white", fg="#FFBA00", anchor="w")
    label1.grid(row=0, column=0, columnspan=3, sticky="new")

    FoodItemReviews.columnconfigure(0, weight=1)
    FoodItemReviews.columnconfigure(1, weight=1)
    FoodItemReviews.rowconfigure(0, weight=1)

    for i in range(3):
        FoodItemReviews.columnconfigure(i, weight=1)
        FoodItemReviews.rowconfigure(i + 1, weight=1)

    reviews = fetch_reviews(item_id)
    for review in reviews:
        create_new_box(review)

    button_frame = ttk.Frame(FoodItemReviews)
    button_frame.grid(row=4, column=0, columnspan=3, pady=20)

    add_button = ttk.Button(button_frame, text="Add New Review", command=add_review)
    add_button.grid(row=0, column=0, padx=10)

    back_button = ttk.Button(button_frame, text="Back", command=go_back)
    back_button.grid(row=0, column=1, padx=10)

    FoodItemReviews.mainloop()