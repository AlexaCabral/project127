from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class ReviewWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Reviews")
        self.root.geometry("1100x550+0+90")
        self.root.resizable(False, False)
        self.root.configure(bg="white")
    
        # title
        title_label = Label(self.root, text="Review Details", font=('Courier', 25, 'bold'), bg="#FFBA00", fg="#725B32")
        title_label.pack(fill="x")

        # ========== left-side ==========
        frame_label_left =LabelFrame(self.root, bd=2, relief=RIDGE, text="Establishments and Food Items", font=('Courier', 13, 'bold'), padx=2, bg="white")
        frame_label_left.place(x=0, y=45, width=425, height=500)
        
        # search label
        search_label = Label(frame_label_left, text="Establishment Name:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        search_label.grid(row=0, column=0, sticky=W, padx=2)
        
        # search box for establishment
        self.var_search_establishment = StringVar()
        search_entry = ttk.Entry(frame_label_left, font=('Courier', 12, 'bold'), width=14, textvariable=self.var_search_establishment)
        search_entry.grid(row=0, column=1, padx=2)
        
         # search button
        search_btn = Button(frame_label_left, text="Search", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=6, command=self.search)
        search_btn.grid(row=0, column=2, padx=1)

        # ====================== results left establishment ======================
        left_frame = Frame(frame_label_left, relief=RIDGE)
        left_frame.place(x=0, y=30, width=418, height=200)
        
        scroll_x = ttk.Scrollbar(left_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(left_frame, orient=VERTICAL)
        
        self.Establishment_Table = ttk.Treeview(left_frame, column=("establishment_id", "location", "description", "average_rating", "name"), xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill="x")
        scroll_y.pack(side=RIGHT, fill="y")
        
        scroll_x.config(command=self.Establishment_Table.xview)
        scroll_y.config(command=self.Establishment_Table.yview)
        
        # heading
        self.Establishment_Table.heading("establishment_id", text="ID")
        self.Establishment_Table.heading("name", text="Name")
        self.Establishment_Table.heading("location", text="Location")
        self.Establishment_Table.heading("description", text="Description")
        self.Establishment_Table.heading("average_rating", text="Average Rating")
        
        self.Establishment_Table["show"] = "headings"

        # columns
        self.Establishment_Table.column("establishment_id", width=100)
        self.Establishment_Table.column("name", width=100)
        self.Establishment_Table.column("location", width=100)
        self.Establishment_Table.column("description", width=100)
        self.Establishment_Table.column("average_rating", width=100)

        self.Establishment_Table.pack(fill=BOTH, expand=1)
        self.Establishment_Table.bind("<ButtonRelease-1>", self.get_id)
        self.fetch_data()
        
        # left side Food items
        
        # label ID
        id_label_left = Label(frame_label_left, text="ID:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        id_label_left.place(x=0, y=252)
        
        # box ID
        self.var_estab_id = StringVar()
        search_entry = ttk.Entry(frame_label_left, font=('Courier', 12, 'bold'), width=3, textvariable=self.var_estab_id, state="readonly")
        search_entry.place(x=38, y=252)
        
        # search label
        search2_label = Label(frame_label_left, text="Food Item Name:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        search2_label.place(x=80, y=252)
        
        # search box for food item
        self.var_search_food_item = StringVar()
        search_entry = ttk.Entry(frame_label_left, font=('Courier', 12, 'bold'), width=10, textvariable=self.var_search_food_item)
        search_entry.place(x=238, y=252)
        
         # search button
        search2_btn = Button(frame_label_left, text="Search", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=6, command=self.search_food_item)
        search2_btn.place(x=351, y=250)
        
        # ====================== results left food items ======================
        left_frame2 = Frame(frame_label_left, relief=RIDGE)
        left_frame2.place(x=0, y=280, width=418, height=200)
        
        scroll_x1 = ttk.Scrollbar(left_frame2, orient=HORIZONTAL)
        scroll_y1 = ttk.Scrollbar(left_frame2, orient=VERTICAL)
        
        self.Fooditem_Table = ttk.Treeview(left_frame2, column=("item_id", "price", "description", "name", "establishment_id"), xscrollcommand=scroll_x1.set, yscrollcommand=scroll_y1.set)
        
        scroll_x1.pack(side=BOTTOM, fill="x")
        scroll_y1.pack(side=RIGHT, fill="y")
        
        scroll_x1.config(command=self.Fooditem_Table.xview)
        scroll_y1.config(command=self.Fooditem_Table.yview)
        
        # heading
        self.Fooditem_Table.heading("item_id", text="ID")
        self.Fooditem_Table.heading("price", text="Price")
        self.Fooditem_Table.heading("description", text="Description")
        self.Fooditem_Table.heading("name", text="Name")
        self.Fooditem_Table.heading("establishment_id", text="Establishment ID")
        
        self.Fooditem_Table["show"] = "headings"
        
        # columns
        self.Fooditem_Table.column("item_id", width=100)
        self.Fooditem_Table.column("price", width=100)
        self.Fooditem_Table.column("description", width=100)
        self.Fooditem_Table.column("name", width=100)
        self.Fooditem_Table.column("establishment_id", width=100)

        self.Fooditem_Table.pack(fill=BOTH, expand=1)
        self.Fooditem_Table.bind("<ButtonRelease-1>", self.get_idfood)
        self.fetch_data_fooditem()
        
        # ========== right-side ==========
        frame_label_right =LabelFrame(self.root, bd=2, relief=RIDGE, text="View Review Details", font=('Courier', 13, 'bold'), padx=2, bg="white")
        frame_label_right.place(x=425, y=45, width=673, height=500)
        
        # label ID
        id_label_right = Label(frame_label_right, text="Establishment ID:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        id_label_right.grid(row=0, column=0, sticky=W, padx=2)
        
        # box ID
        self.var_estab_id_right = StringVar()
        search_entry = ttk.Entry(frame_label_right, font=('Courier', 12, 'bold'), width=4, textvariable=self.var_estab_id_right, state="readonly")
        search_entry.grid(row=0, column=1, padx=2)
        
        # label food item ID
        food_item_id_label_right = Label(frame_label_right, text="Food Item ID:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        food_item_id_label_right.grid(row=0, column=3, sticky=W, padx=2)
        
        # box food item ID
        self.var_food_id = StringVar()
        search_entry = ttk.Entry(frame_label_right, font=('Courier', 12, 'bold'), width=4, textvariable=self.var_food_id, state="readonly")
        search_entry.grid(row=0, column=4, padx=2)
        
        # label filter month
        food_item_id_label_right = Label(frame_label_right, text="Month:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        food_item_id_label_right.grid(row=0, column=6, sticky=W, padx=2)
        
        # dropdown filter month
        self.var_filter_dropdown = StringVar()
        filter_search = ttk.Combobox(frame_label_right, font=('Courier', 12, 'bold'), width=10, state="readonly", textvariable=self.var_filter_dropdown)
        filter_search["value"] = ("", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
        filter_search.current(0)
        filter_search.grid(row=0, column=7)
        
        # search button
        searchreview_btn = Button(frame_label_right, text="Search", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=29, command=self.search_review)
        searchreview_btn.place(x=5, y=28)
        
        # clear button
        clear_btn = Button(frame_label_right, text="Clear", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=29, command=self.clear_filter)
        clear_btn.place(x=315, y=28)
        
        # ====================== results right ======================
        data_frame = Frame(frame_label_right, relief=RIDGE)
        data_frame.place(x=0, y=70, width=660, height=400)
        
        scroll_x2 = ttk.Scrollbar(data_frame, orient=HORIZONTAL)
        scroll_y2 = ttk.Scrollbar(data_frame, orient=VERTICAL)
        
        self.Review_Table = ttk.Treeview(data_frame, column=("review_id", "review_text", "rating", "datetime", "account_id", "establishment_id", "item_id"), xscrollcommand=scroll_x2.set, yscrollcommand=scroll_y2.set)
        
        scroll_x2.pack(side=BOTTOM, fill="x")
        scroll_y2.pack(side=RIGHT, fill="y")
        
        scroll_x2.config(command=self.Review_Table.xview)
        scroll_y2.config(command=self.Review_Table.yview)
        
        # heading
        self.Review_Table.heading("review_id", text="ID")
        self.Review_Table.heading("review_text", text="Review Text")
        self.Review_Table.heading("rating", text="Rating")
        self.Review_Table.heading("datetime", text="Date And Time")
        self.Review_Table.heading("account_id", text="Account ID")
        self.Review_Table.heading("establishment_id", text="Establishment ID")
        self.Review_Table.heading("item_id", text="Item ID")
        
        self.Review_Table["show"] = "headings"
        
         # columns
        self.Review_Table.column("review_id", width=100)
        self.Review_Table.column("review_text", width=100)
        self.Review_Table.column("rating", width=100)
        self.Review_Table.column("datetime", width=150)
        self.Review_Table.column("account_id", width=100)
        self.Review_Table.column("establishment_id", width=100)
        self.Review_Table.column("item_id", width=100)

        self.Review_Table.pack(fill=BOTH, expand=1)
        self.fetch_data_reviews()
        
        
    # ====================== back end ======================
    # show data establishment
    def fetch_data(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
                
            mycursor.execute("SELECT * FROM food_establishment")
            rows = mycursor.fetchall()
            print("Query")
                
            if len(rows) != 0:
                self.Establishment_Table.delete(*self.Establishment_Table.get_children())
                for i in rows:
                    self.Establishment_Table.insert("", END, values=i)
                mydb.commit()
            else:
                self.Establishment_Table.delete(*self.Establishment_Table.get_children())
                mydb.commit()
                
            mydb.close()
                     
        except:
            messagebox.showerror("Connection", "Failed")
            return
    
    def get_id(self, event=""):
        cursor_row = self.Establishment_Table.focus()
        content = self.Establishment_Table.item(cursor_row)
        row = content["values"]

        self.var_estab_id.set(row[0])
        self.var_estab_id_right.set(row[0])
        
    def get_idfood(self, event=""):
        cursor_row = self.Fooditem_Table.focus()
        content = self.Fooditem_Table.item(cursor_row)
        row = content["values"]

        self.var_food_id.set(row[0])
    
    # show data food items
    def fetch_data_fooditem(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
                
            mycursor.execute("SELECT * FROM food_item")
            rows = mycursor.fetchall()
            print("Query")
                
            if len(rows) != 0:
                self.Fooditem_Table.delete(*self.Fooditem_Table.get_children())
                for i in rows:
                    self.Fooditem_Table.insert("", END, values=i)
                mydb.commit()
            else:
                self.Fooditem_Table.delete(*self.Fooditem_Table.get_children())
                mydb.commit()
                
            mydb.close()
                     
        except:
            messagebox.showerror("Connection", "Failed")
            return
        
    # show data reviews
    def fetch_data_reviews(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
                
            mycursor.execute("SELECT * FROM food_review")
            rows = mycursor.fetchall()
            print("Query")
                
            if len(rows) != 0:
                self.Review_Table.delete(*self.Review_Table.get_children())
                for i in rows:
                    self.Review_Table.insert("", END, values=i)
                mydb.commit()
            mydb.close()
                     
        except:
            messagebox.showerror("Connection", "Failed")
            return
    
    # search for establishments
    def search(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
                
            mycursor.execute("SELECT * FROM food_establishment where name LIKE '%"+str(self.var_search_establishment.get())+"%'")
            rows = mycursor.fetchall()
            print("Query")
                
            if len(rows) != 0:
                self.Establishment_Table.delete(*self.Establishment_Table.get_children())
                for i in rows:
                    self.Establishment_Table.insert("", END, values=i)
                mydb.commit()
            else:
                self.Establishment_Table.delete(*self.Establishment_Table.get_children())
                mydb.commit()
                
            mydb.close()
                 
        except:
            messagebox.showerror("Connection", "Failed")
            return
    
    def search_food_item(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
            
            # no id
            if(self.var_estab_id.get() == ""):
                print("No establishment ID")
                mycursor.execute("SELECT * FROM food_item WHERE name LIKE '%"+str(self.var_search_food_item.get())+"%'")
                rows = mycursor.fetchall()
                print("Query")
            else:
                print("SELECT * FROM food_item WHERE name LIKE '%"+str(self.var_search_food_item.get())+"%' and establishmet_id = "+str(self.var_estab_id.get()))
                mycursor.execute("SELECT * FROM food_item WHERE name LIKE '%"+str(self.var_search_food_item.get())+"%' and establishment_id = "+str(self.var_estab_id.get()))
                rows = mycursor.fetchall()
                
            
                
            if len(rows) != 0:
                self.Fooditem_Table.delete(*self.Fooditem_Table.get_children())
                for i in rows:
                    self.Fooditem_Table.insert("", END, values=i)
                mydb.commit()
            else:
                self.Fooditem_Table.delete(*self.Fooditem_Table.get_children())
                mydb.commit()
                
            mydb.close()
                 
        except:
            messagebox.showerror("Connection", "Failed")
            return
    def search_review(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
            
            query1 = "SELECT * FROM food_review"
            if(self.var_estab_id_right.get() == "" and self.var_food_id.get() == ""):
                if(self.var_filter_dropdown.get() == ""):
                    print("No filter")
                    mycursor.execute(query1)
                    rows = mycursor.fetchall()
                else:
                    print("Filter")
                    mycursor.execute(query1+" WHERE MONTHNAME(datetime) LIKE '"+str(self.var_filter_dropdown.get())+"'")
                    rows = mycursor.fetchall()
            elif(self.var_estab_id_right.get() != "" and self.var_food_id.get() == ""):
                if(self.var_filter_dropdown.get() == ""):
                    print("No filter, estab id")
                    mycursor.execute(query1+" WHERE establishment_id = "+str(self.var_estab_id_right.get()))
                    rows = mycursor.fetchall()
                else:
                    print("Filter, estab id")
                    mycursor.execute(query1+" WHERE MONTHNAME(datetime) LIKE '"+str(self.var_filter_dropdown.get())+"' AND establishment_id ="+str(self.var_estab_id_right.get()))
                    rows = mycursor.fetchall()
                    
            elif(self.var_estab_id_right.get() == "" and self.var_food_id.get() != ""):
                if(self.var_filter_dropdown.get() == ""):
                    print("No filter, food id")
                    mycursor.execute(query1+" WHERE item_id ="+str(self.var_food_id.get()))
                    rows = mycursor.fetchall()
                else:
                    print("Filter, food id")
                    mycursor.execute(query1+" WHERE MONTHNAME(datetime) LIKE '"+str(self.var_filter_dropdown.get())+"' and item_id ="+str(self.var_food_id.get()))
                    rows = mycursor.fetchall()
            else:
                if(self.var_filter_dropdown.get() == ""):
                    print("No filter, food id, estab id")
                    mycursor.execute(query1+" WHERE item_id ="+str(self.var_food_id.get())+" AND establishment_id ="+str(self.var_estab_id_right.get()))
                    rows = mycursor.fetchall()
                else:
                    print("Filter, food id, estab id")
                    mycursor.execute(query1+" WHERE MONTHNAME(datetime) LIKE '"+str(self.var_filter_dropdown.get())+"' and item_id ="+str(self.var_food_id.get())+" AND establishment_id ="+str(self.var_estab_id_right.get()))
                    rows = mycursor.fetchall()
            
            if len(rows) != 0:
                self.Review_Table.delete(*self.Review_Table.get_children())
                for i in rows:
                    self.Review_Table.insert("", END, values=i)
                mydb.commit()
            
            else:
                self.Review_Table.delete(*self.Review_Table.get_children())
                mydb.commit()
                
            mydb.close()
                
        except:
            messagebox.showerror("Connection", "Failed")
            return
    
    def clear_filter(self):
        self.var_estab_id.set("")
        self.var_estab_id_right.set("")
        self.var_filter_dropdown.set("")
        self.var_food_id.set("")


if __name__ == "__main__":
    root=Tk()
    obj = ReviewWindow(root)
    root.mainloop()