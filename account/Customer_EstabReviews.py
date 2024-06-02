import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import Customer_FoodItems


def establishmentReviews(parent, establishment_id, account_id):

    def fetch_reviews(estab_id):
        try:
            database = mysql.connector.connect(
                host="localhost",
                user="root",
                password="chancekababy2021",
                database="project",
            )
            database_cursor = database.cursor()
            print("Connected to database...")
        except mysql.connector.Error as err:
            messagebox.showerror("Connection", f"Failed: {err}")
            return []

        query = f"SELECT review_id, review_text, rating FROM food_review WHERE establishment_id = {estab_id} AND account_id = {account_id}"
        database_cursor.execute(query)
        results = database_cursor.fetchall()

        database_cursor.close()
        database.close()

        reviews = [
            {
                "review_id": r[0],
                "review_text": r[1],
                "rating": r[2],
                "account_id": account_id,
                "establishment_id": establishment_id,
            }
            for r in results
        ]
        return reviews

    def add_review_to_db(review):
        try:
            database = mysql.connector.connect(
                host="localhost",
                user="root",
                password="chancekababy2021",
                database="project",
            )
            database_cursor = database.cursor()
            print("Connected to database...")
        except mysql.connector.Error as err:
            messagebox.showerror("Connection", f"Failed: {err}")
            return None

        query = "INSERT INTO food_review (review_text, rating, account_id, establishment_id) VALUES (%s, %s, %s, %s)"
        database_cursor.execute(
            query,
            (
                review["review_text"],
                review["rating"],
                account_id,
                establishment_id,
            ),
        )
        database.commit()

        review_id = database_cursor.lastrowid
        database_cursor.close()
        database.close()

        return review_id

    def update_review_in_db(review):
        try:
            database = mysql.connector.connect(
                host="localhost",
                user="root",
                password="chancekababy2021",
                database="project",
            )
            database_cursor = database.cursor()
            print("Connected to database...")
        except mysql.connector.Error as err:
            messagebox.showerror("Connection", f"Failed: {err}")
            return

        query = "UPDATE food_review SET review_text = %s, rating = %s WHERE review_id = %s"
        database_cursor.execute(
            query,
            (
                review["review_text"],
                review["rating"],
                review["review_id"],
            ),
        )
        database.commit()

        database_cursor.close()
        database.close()

    def delete_review_from_db(review_id):
        try:
            database = mysql.connector.connect(
                host="localhost",
                user="root",
                password="chancekababy2021",
                database="project",
            )
            database_cursor = database.cursor()
            print("Connected to database...")
        except mysql.connector.Error as err:
            messagebox.showerror("Connection", f"Failed: {err}")
            return

        query = "DELETE FROM food_review WHERE review_id = %s"
        database_cursor.execute(query, (review_id,))
        database.commit()

        database_cursor.close()
        database.close()

    def add_review():
        dialog = AddReviewDialog(estabReviews)
        estabReviews.wait_window(dialog.top)
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

            tk.Label(self.top, text="Review Text:").pack()
            self.review_text_entry = ttk.Entry(self.top)
            self.review_text_entry.pack()

            tk.Label(self.top, text="Rating (1-5):").pack()
            self.rating_entry = ttk.Entry(self.top)
            self.rating_entry.pack()

            ttk.Button(self.top, text="Add", command=self.add).pack()

        def add(self):
            self.result = {
                "review_text": self.review_text_entry.get(),
                "rating": int(self.rating_entry.get()),
                "account_id": account_id,
                "establishment_id": establishment_id,
            }
            self.top.destroy()

    class EditReviewDialog:
        def __init__(self, parent, review):
            self.top = tk.Toplevel(parent)
            self.top.title("Edit Review")
            self.top.geometry("300x300")
            self.result = None
            self.review = review

            tk.Label(self.top, text="Review Text:").pack()
            self.review_text_entry = ttk.Entry(self.top)
            self.review_text_entry.pack()
            self.review_text_entry.insert(0, review["review_text"])

            tk.Label(self.top, text="Rating (1-5):").pack()
            self.rating_entry = ttk.Entry(self.top)
            self.rating_entry.pack()
            self.rating_entry.insert(0, review["rating"])

            ttk.Button(self.top, text="Update", command=self.update).pack()

        def update(self):
            self.result = {
                "review_id": self.review["review_id"],
                "review_text": self.review_text_entry.get(),
                "rating": int(self.rating_entry.get())
            }
            self.top.destroy()

    def create_new_box(review):
        new_box_frame = ttk.Frame(estabReviews, borderwidth=1, relief="solid")
        total_boxes = len(estabReviews.grid_slaves()) - 1
        row_position = total_boxes // 3 + 1
        column_position = total_boxes % 3

        new_box_frame.grid(
            row=row_position, column=column_position, padx=20, pady=30, sticky="nsew"
        )

        reviewer_name_label = tk.Label(new_box_frame, text=review["account_id"])
        reviewer_name_label.pack(expand=True)

        details_label = tk.Label(
            new_box_frame,
            text=f"ID: {review['review_id']}\nRating: {review['rating']}\nReview: {review['review_text']}\nEstablishment: {review['establishment_id']}",
        )
        details_label.pack(expand=True)

        edit_button = ttk.Button(
            new_box_frame,
            text="Edit",
            command=lambda: edit_review(new_box_frame, review),
        )
        edit_button.pack(side="left", padx=5)

        delete_box_button = ttk.Button(
            new_box_frame,
            text="Delete",
            command=lambda: delete_box(new_box_frame, review["review_id"]),
        )
        delete_box_button.pack(side="left", padx=5)

        if total_boxes % 3 == 2:
            estabReviews.grid_rowconfigure(row_position + 1, weight=1)

    def delete_box(box_frame, review_id):
        delete_review_from_db(review_id)
        box_frame.destroy()

    def edit_review(box_frame, review):
        dialog = EditReviewDialog(estabReviews, review)
        estabReviews.wait_window(dialog.top)
        if dialog.result:
            update_review_in_db(dialog.result)
            review.update(dialog.result)
            for widget in box_frame.winfo_children():
                widget.destroy()

            reviewer_name_label = tk.Label(box_frame, text=review["account_id"])
            reviewer_name_label.pack(expand=True)

            details_label = tk.Label(
                box_frame,
                text=f"ID: {review['review_id']}\nRating: {review['rating']}\nReview: {review['review_text']}\nEstablishment: {review['establishment_id']}",
            )
            details_label.pack(expand=True)

            edit_button = ttk.Button(
                box_frame, text="Edit", command=lambda: edit_review(box_frame, review)
            )
            edit_button.pack(side="left", padx=5)

            delete_box_button = ttk.Button(
                box_frame,
                text="Delete",
                command=lambda: delete_box(box_frame, review["review_id"]),
            )
            delete_box_button.pack(side="left", padx=5)

    def go_back():
        parent.deiconify()
        estabReviews.destroy()

    def view_food_items():
        print("Food Items button clicked")
        estabReviews.withdraw()
        Customer_FoodItems.FoodReviews(estabReviews, account_id, establishment_id)

    estabReviews = tk.Tk()
    estabReviews.geometry("1100x650")
    estabReviews.title("Food Establishment Reviews")
    estabReviews.resizable(False, False)

    estabReviews.configure(bg="#D3D3D3")

    label1 = tk.Label(
        estabReviews,
        text="Food Establishment Reviews",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#FFBA00",
        anchor="w",
    )
    label1.grid(row=0, column=0, columnspan=3, sticky="new")

    estabReviews.columnconfigure(0, weight=1)
    estabReviews.columnconfigure(1, weight=1)
    estabReviews.columnconfigure(2, weight=1)

    backButton = tk.Button(
        estabReviews,
        text="Back",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#FFBA00",
        command=go_back,
    )
    backButton.grid(row=5, column=1, pady=20)

    addButton = tk.Button(
        estabReviews,
        text="Add Review",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#FFBA00",
        command=add_review,
    )
    addButton.grid(row=5, column=2, pady=20)

    viewItemsButton = tk.Button(
        estabReviews,
        text="Food Items",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#FFBA00",
        command=view_food_items,
    )
    viewItemsButton.grid(row=5, column=0, pady=20)

    reviews = fetch_reviews(establishment_id)
    for review in reviews:
        create_new_box(review)

    estabReviews.mainloop()
