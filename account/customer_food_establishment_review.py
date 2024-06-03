import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import customer_food_item


def customer_food_establishment_review(parent, establishment_id, account_id):
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

    def search_food_establishment_review():
        database = connect_to_db()
        if not database:
            return []
        database_cursor = database.cursor()

        query = f"SELECT review_id, review_text, rating FROM food_review WHERE establishment_id = {establishment_id} AND account_id = {account_id}"
        database_cursor.execute(query)
        results = database_cursor.fetchall()
        database_cursor.close()
        database.close()
        return results

    def update_average_rating():
        database = connect_to_db()
        if not database:
            return []
        database_cursor = database.cursor()

        query = "SELECT AVG(rating) FROM food_review WHERE establishment_id = %s"
        database_cursor.execute(query, (establishment_id,))
        new_avg_rating = database_cursor.fetchone()[0]

        query = "UPDATE food_establishment SET average_rating = %s WHERE establishment_id = %s"
        database_cursor.execute(
            query,
            (
                new_avg_rating,
                establishment_id,
            ),
        )
        database.commit()
        database_cursor.close()
        database.close()

    def add_review_to_db(review):
        database = connect_to_db()
        if not database:
            return []
        database_cursor = database.cursor()

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

        update_average_rating()

        return review_id

    def update_review_in_db(review):
        database = connect_to_db()
        if not database:
            return []
        database_cursor = database.cursor()

        query = (
            "UPDATE food_review SET review_text = %s, rating = %s WHERE review_id = %s"
        )
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

        update_average_rating()

    def delete_review_from_db(review_id):
        database = connect_to_db()
        if not database:
            return []
        database_cursor = database.cursor()

        query = "DELETE FROM food_review WHERE review_id = %s"
        database_cursor.execute(query, (review_id,))
        database.commit()

        database_cursor.close()
        database.close()

        update_average_rating()

    def add_review():
        dialog = AddReviewDialog(customer_food_establishment_review_window)
        customer_food_establishment_review_window.wait_window(dialog.top)
        if dialog.result:
            review_id = add_review_to_db(dialog.result)
            if review_id:
                dialog.result["review_id"] = review_id
                create_new_box(dialog.result)

    class AddReviewDialog:
        def __init__(self, parent):
            self.top = tk.Toplevel(parent)
            self.top.title("Add New Review")
            self.top.geometry("600x600")
            self.result = None

            tk.Label(self.top, text="Review Text:").pack(pady=(20, 5))
            self.review_text_entry = tk.Text(self.top, height=10, width=40)
            self.review_text_entry.pack(pady=(0, 20))

            tk.Label(self.top, text="Rating (1-5):").pack(pady=(0, 5))
            self.rating_entry = ttk.Entry(self.top)
            self.rating_entry.pack(pady=(0, 20))

            ttk.Button(self.top, text="Add", command=self.add).pack(pady=(20, 0))

        def add(self):
            try:
                rating = int(self.rating_entry.get())
                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be an integer between 1 and 5.")
                self.result = {
                    "review_text": self.review_text_entry.get("1.0", tk.END).strip(),
                    "rating": int(self.rating_entry.get()),
                    "account_id": account_id,
                    "establishment_id": establishment_id,
                }
                self.top.destroy()
            except ValueError as e:
                messagebox.showerror("Invalid Rating", str(e))

    class EditReviewDialog:
        def __init__(self, parent, review):
            self.top = tk.Toplevel(parent)
            self.top.title("Edit Review")
            self.top.geometry("600x600")
            self.result = None
            self.review = review

            tk.Label(self.top, text="Review Text:").pack(pady=(20, 5))
            self.review_text_entry = tk.Text(self.top, height=10, width=40)
            self.review_text_entry.pack(pady=(0, 20))
            self.review_text_entry.insert(tk.END, review["review_text"])

            tk.Label(self.top, text="Rating (1-5):").pack(pady=(0, 5))
            self.rating_entry = ttk.Entry(self.top)
            self.rating_entry.pack(pady=(0, 20))
            self.rating_entry.insert(0, review["rating"])

            ttk.Button(self.top, text="Update", command=self.update).pack(pady=(20, 0))

        def update(self):
            try:
                rating = int(self.rating_entry.get())
                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be an integer between 1 and 5.")
                self.result = {
                    "review_id": self.review["review_id"],
                    "review_text": self.review_text_entry.get("1.0", tk.END).strip(),
                    "rating": int(self.rating_entry.get()),
                }
                self.top.destroy()
            except ValueError as e:
                messagebox.showerror("Invalid Rating", str(e))

    def create_new_box(review):
        new_box_frame = tk.Frame(
            boxes_frame,
            bg="#FFFFFF",
            borderwidth=1,
            relief="solid",
            width=300,
            height=250,
        )
        new_box_frame.grid_propagate(False)
        new_box_frame.columnconfigure(0, weight=1)
        total_boxes = len(boxes_frame.grid_slaves())
        row_position = total_boxes // 3
        column_position = total_boxes % 3

        new_box_frame.grid(
            row=row_position, column=column_position, padx=20, pady=30, sticky="nsew"
        )

        container = tk.Frame(new_box_frame, bg="#FFFFFF", bd=0)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        review_id_label = tk.Label(
            container,
            bg="#FFFFFF",
            text="Review ID",
            font=("Helvetica", 10, "bold"),
            fg="#B46617",
        )
        review_id_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        review_id_value_label = tk.Label(
            container,
            bg="#FFFFFF",
            text=review["review_id"],
            font=("Helvetica Neue Light", 10),
            fg="#B46617",
        )
        review_id_value_label.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        rating_label = tk.Label(
            container,
            bg="#FFFFFF",
            text="Rating",
            font=("Helvetica", 10, "bold"),
            fg="#B46617",
        )
        rating_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        rating_value_label = tk.Label(
            container,
            bg="#FFFFFF",
            text=review["rating"],
            font=("Helvetica Neue Light", 10),
            fg="#B46617",
        )
        rating_value_label.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        review_text_label = tk.Label(
            new_box_frame,
            bg="#FFFFFF",
            text="Review text",
            font=("Helvetica", 10, "bold"),
            fg="#B46617",
        )
        review_text_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        review_text_text = tk.Text(
            new_box_frame,
            bg="#FFFFFF",
            font=("Helvetica Neue Light", 10),
            wrap="word",
            height=5,
            bd=0,
            fg="#B46617",
        )
        review_text_text.insert(tk.END, review["review_text"])
        review_text_text.configure(state="disabled")
        review_text_text.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        edit_button = tk.Button(
            new_box_frame,
            text="Edit",
            font=("Helvetica", 10),
            command=lambda: edit_review(review),
            bg="#B46617",
            fg="white",
            bd=0,
        )
        edit_button.grid(row=3, column=0, columnspan=1, pady=5, sticky="s")

        delete_box_button = tk.Button(
            new_box_frame,
            text="Delete",
            font=("Helvetica", 10),
            command=lambda: delete_box(new_box_frame, review["review_id"]),
            bg="#B46617",
            fg="white",
            bd=0,
        )
        delete_box_button.grid(row=4, column=0, columnspan=1, pady=5, sticky="s")

        if total_boxes % 3 == 2:
            customer_food_establishment_review_window.grid_rowconfigure(
                row_position + 1, weight=1
            )

    def delete_box(box_frame, review_id):
        delete_review_from_db(review_id)
        box_frame.destroy()

    def edit_review(review):
        dialog = EditReviewDialog(customer_food_establishment_review_window, review)
        customer_food_establishment_review_window.wait_window(dialog.top)
        if dialog.result:
            update_review_in_db(dialog.result)
            review.update(dialog.result)
            load_initial_data()

    def go_back():
        parent.deiconify()
        customer_food_establishment_review_window.destroy()

    def view_food_items():
        print("Food Items button clicked")
        customer_food_establishment_review_window.withdraw()
        customer_food_item.customer_food_item(
            customer_food_establishment_review_window, account_id, establishment_id
        )

    def clear_boxes():
        for widget in boxes_frame.grid_slaves():
            widget.destroy()

    def load_initial_data():
        clear_boxes()
        establishment_reviews = search_food_establishment_review()
        for establishment_review in establishment_reviews:
            establishment_review = {
                "review_id": establishment_review[0],
                "review_text": establishment_review[1],
                "rating": establishment_review[2],
            }
            create_new_box(establishment_review)

    customer_food_establishment_review_window = tk.Tk()
    customer_food_establishment_review_window.geometry("1100x650")
    customer_food_establishment_review_window.title("Food Establishment Reviews")
    customer_food_establishment_review_window.resizable(False, False)
    customer_food_establishment_review_window.configure(bg="#FFFFFF")

    label1 = tk.Label(
        customer_food_establishment_review_window,
        text="FOOD ESTABLISHMENT REVIEWS",
        font=("Helvetica", 20, "bold"),
        bg="white",
        fg="#FFBA00",
        anchor="n",
    )
    label1.grid(row=0, column=0, columnspan=3, sticky="new", pady=10)

    canvas = tk.Canvas(customer_food_establishment_review_window, bg="#FFFFFF")
    scroll_y = tk.Scrollbar(
        customer_food_establishment_review_window,
        orient="vertical",
        command=canvas.yview,
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

    back_button = tk.Button(
        customer_food_establishment_review_window,
        text="Back",
        font=("Arial", 12, "bold"),
        bg="#B46617",
        fg="white",
        command=go_back,
        bd=0,
    )
    back_button.grid(row=5, column=1, pady=20)

    add_button = tk.Button(
        customer_food_establishment_review_window,
        text="Add Review",
        font=("Arial", 12, "bold"),
        bg="#B46617",
        fg="white",
        command=add_review,
        bd=0,
    )
    add_button.grid(row=5, column=2, pady=20)

    view_items_button = tk.Button(
        customer_food_establishment_review_window,
        text="Food Items",
        font=("Arial", 12, "bold"),
        bg="#B46617",
        fg="white",
        command=view_food_items,
        bd=0,
    )
    view_items_button.grid(row=5, column=0, pady=20)

    customer_food_establishment_review_window.columnconfigure(0, weight=1)
    customer_food_establishment_review_window.columnconfigure(1, weight=1)
    customer_food_establishment_review_window.columnconfigure(2, weight=1)
    customer_food_establishment_review_window.rowconfigure(5, weight=1)

    load_initial_data()
    customer_food_establishment_review_window.mainloop()
