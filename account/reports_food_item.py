from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


class FoodItemWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Items")
        self.root.geometry("1100x550+0+90")
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        
        # title
        title_label = Label(self.root, text="Food Item Details", font=('Courier', 25, 'bold'), bg="#FFBA00", fg="#725B32")
        title_label.pack(fill="x")
        
        # ========== left-side ==========
        frame_label_left =LabelFrame(self.root, bd=2, relief=RIDGE, text="Establishments", font=('Courier', 13, 'bold'), padx=2, bg="white")
        frame_label_left.place(x=0, y=45, width=425, height=500)
        
        # search label
        search_label = Label(frame_label_left, text="Establishment Name:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        search_label.grid(row=0, column=0, sticky=W, padx=2)
        
        # search box
        self.var_search_text = StringVar()
        search_entry = ttk.Entry(frame_label_left, font=('Courier', 12, 'bold'), width=14, textvariable=self.var_search_text)
        search_entry.grid(row=0, column=1, padx=2)
        
        # search button
        search_btn = Button(frame_label_left, text="Search", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=6, command=self.search)
        search_btn.grid(row=0, column=2, padx=1)
        
         # ====================== results left ======================
        establishment_frame = Frame(frame_label_left, relief=RIDGE)
        establishment_frame.place(x=0, y=30, width=418, height=440)
        
        scroll_x = ttk.Scrollbar(establishment_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(establishment_frame, orient=VERTICAL)
        
        self.Establishment_Table = ttk.Treeview(establishment_frame, column=("establishment_id", "location", "description", "average_rating", "name"), xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
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
        
        
        # ========== right-side ==========
        frame_label_right =LabelFrame(self.root, bd=2, relief=RIDGE, text="View Food Item Details", font=('Courier', 13, 'bold'), padx=2, bg="white")
        frame_label_right.place(x=425, y=45, width=673, height=500)
        
        # label ID
        id_label = Label(frame_label_right, text="ID:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        id_label.grid(row=0, column=0, sticky=W, padx=2)
        
        # box ID
        self.var_estab_id = StringVar()
        search_entry = ttk.Entry(frame_label_right, font=('Courier', 12, 'bold'), width=4, textvariable=self.var_estab_id, state="readonly")
        search_entry.grid(row=0, column=1, padx=2)
    
        # sort label price
        sort_labelprice = Label(frame_label_right, text="Sort By:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        sort_labelprice.grid(row=0, column=2, padx=2)
        
        # drop down sort
        self.var_sort_dropdown = StringVar()
        sort_search = ttk.Combobox(frame_label_right, font=('Courier', 12, 'bold'), width=10, state="readonly", textvariable=self.var_sort_dropdown)
        sort_search["value"] = ("", "High Price", "Low Price")
        sort_search.current(0)
        sort_search.grid(row=0, column=3)
        
        # search food type label
        search_labelfood = Label(frame_label_right, text="Food Type:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        search_labelfood.grid(row=0, column=4, padx=2)
        
        self.var_search_text_food_type = StringVar()
        search_entry = ttk.Entry(frame_label_right, font=('Courier', 12, 'bold'), width=23, textvariable=self.var_search_text_food_type)
        search_entry.grid(row=0, column=5, padx=2)
        
        # staring price label
        range_label = Label(frame_label_right, text="Price Range:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#725B32")
        range_label.place(x=0, y=30)
        
        self.var_start_price = StringVar()
        range_entry = Entry(frame_label_right, font=('Courier', 12, 'bold'), width=5, textvariable=self.var_start_price)
        range_entry.place(x=130, y=30)
        
        range_label = Label(frame_label_right, text="-", font=('Courier', 12, 'bold'), fg="#725B32", bg="white")
        range_label.place(x=185, y=30)
        
        self.var_end_price = StringVar()
        range2_entry = Entry(frame_label_right, font=('Courier', 12, 'bold'), width=5, textvariable=self.var_end_price)
        range2_entry.place(x=205, y=30)
        
         # search button
        searchfood_btn = Button(frame_label_right, text="Search", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=8, command=self.search_food)
        searchfood_btn.place(x=470, y=28)
        
         # clear button
        clear_btn = Button(frame_label_right, text="Clear", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#725B32", activeforeground="white", cursor="hand2", width=8, command=self.clear_filter)
        clear_btn.place(x=565, y=28)
   
        
        # ====================== results right ======================
        data_frame = Frame(frame_label_right, relief=RIDGE)
        data_frame.place(x=0, y=70, width=660, height=400)
        
        scroll_x1 = ttk.Scrollbar(data_frame, orient=HORIZONTAL)
        scroll_y1 = ttk.Scrollbar(data_frame, orient=VERTICAL)
        
        self.Fooditem_Table = ttk.Treeview(data_frame, column=("item_id", "price", "description", "name", "establishment_id"), xscrollcommand=scroll_x1.set, yscrollcommand=scroll_y1.set)
        
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
        self.fetch_data_fooditem()
        
        
        
        
    # ====================== back end ======================
    # show data food item
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
            mydb.close()
                     
        except:
            messagebox.showerror("Connection", "Failed")
            return
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
            mydb.close()
                     
        except:
            messagebox.showerror("Connection", "Failed")
            return
    
    def search(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
                
            mycursor.execute("SELECT * FROM food_establishment where name LIKE '%"+str(self.var_search_text.get())+"%'")
            rows = mycursor.fetchall()
            print("Query")
                
            if len(rows) != 0:
                self.Establishment_Table.delete(*self.Establishment_Table.get_children())
                for i in rows:
                    self.Establishment_Table.insert("", END, values=i)
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
    
    def sort(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
            
            if (str(self.var_sort_dropdown.get()) == "High Price"):
                mycursor.execute("SELECT * FROM food_item ORDER BY price ASC")
                rows = mycursor.fetchall()
                print("Ascending")
            
            else:
                mycursor.execute("SELECT * FROM food_item ORDER BY price DESC")
                rows = mycursor.fetchall()
                print("Descending")
                
            if len(rows) != 0:
                self.Fooditem_Table.delete(*self.Fooditem_Table.get_children())
                for i in rows:
                    self.Fooditem_Table.insert("", END, values=i)
                mydb.commit()
            mydb.close()
                     
        except:
            messagebox.showerror("Connection", "Failed")
            return
    
    def clear_filter(self):
        self.var_estab_id.set("")
        self.var_sort_dropdown.set("")
        self.var_search_text_food_type.set("")
        self.var_start_price.set("")
        self.var_end_price.set("")
    
    def search_food(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
            
            query1 = "SELECT * FROM food_item WHERE "
            subquery = "(SELECT item_id FROM food_item_food_type WHERE food_type LIKE '%"+str(self.var_search_text_food_type.get())+"%') "
            
            # no id
            if(self.var_estab_id.get() == ""):
                print("No establishment ID")
                # no sort
                if(self.var_sort_dropdown.get() == ""):
                    print("No Order By")
                    # no range
                    if(self.var_start_price.get() == "" and self.var_end_price.get() == ""):
                        print("No range")
                        mycursor.execute(query1+"item_id IN "+subquery)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() != "" and self.var_end_price.get() == ""):
                        print("Start range.")
                        mycursor.execute(query1+"price >= "+str(self.var_start_price.get())+" AND item_id IN "+subquery)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() == "" and self.var_end_price.get() != ""):
                        print("End range.")
                        mycursor.execute(query1+"price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery)
                        rows = mycursor.fetchall()
                    else:
                        print("Start and End range.")
                        mycursor.execute(query1+"price >= "+str(self.var_start_price.get())+" AND price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery)
                        rows = mycursor.fetchall()
                elif(self.var_sort_dropdown.get() == "Low Price"):
                    print("Order BY price ASC")
                    sort_asc = " ORDER BY price ASC"
                    # no range
                    if(self.var_start_price.get() == "" and self.var_end_price.get() == ""):
                        print("No range")
                        mycursor.execute(query1+"item_id IN "+subquery+sort_asc)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() != "" and self.var_end_price.get() == ""):
                        print("Start range.")
                        mycursor.execute(query1+"price >= "+str(self.var_start_price.get())+" AND item_id IN "+subquery+sort_asc)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() == "" and self.var_end_price.get() != ""):
                        print("End range.")
                        mycursor.execute(query1+"price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery+sort_asc)
                        rows = mycursor.fetchall()
                    else:
                        print("Start and End range.")
                        mycursor.execute(query1+"price >= "+str(self.var_start_price.get())+" AND price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery+sort_asc)
                        rows = mycursor.fetchall()
                else:
                    print("Order BY price ASC")
                    sort_desc = " ORDER BY price DESC"
                    # no range
                    if(self.var_start_price.get() == "" and self.var_end_price.get() == ""):
                        print("No range")
                        mycursor.execute(query1+"item_id IN "+subquery+sort_desc)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() != "" and self.var_end_price.get() == ""):
                        print("Start range.")
                        mycursor.execute(query1+"price >= "+str(self.var_start_price.get())+" AND item_id IN "+subquery+sort_desc)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() == "" and self.var_end_price.get() != ""):
                        print("End range.")
                        mycursor.execute(query1+"price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery+sort_desc)
                        rows = mycursor.fetchall()
                    else:
                        print("Start and End range.")
                        mycursor.execute(query1+"price >= "+str(self.var_start_price.get())+" AND price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery+sort_desc)
                        rows = mycursor.fetchall()
            else:
                print("Establishment ID present.")
                
                e_id = str(self.var_estab_id.get())
                establishment_id_condition = "establishment_id ="+e_id+" and "
                # no sort
                if(self.var_sort_dropdown.get() == ""):
                    print("No Order By")
                    # no range
                    if(self.var_start_price.get() == "" and self.var_end_price.get() == ""):
                        print("No range")
                        mycursor.execute(query1+establishment_id_condition+"item_id IN "+subquery)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() != "" and self.var_end_price.get() == ""):
                        print("Start range.")
                        mycursor.execute(query1+establishment_id_condition+"price >= "+str(self.var_start_price.get())+" AND item_id IN "+subquery)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() == "" and self.var_end_price.get() != ""):
                        print("End range.")
                        mycursor.execute(query1+establishment_id_condition+"price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery)
                        rows = mycursor.fetchall()
                    else:
                        print("Start and End range.")
                        mycursor.execute(query1+establishment_id_condition+"price >= "+str(self.var_start_price.get())+" AND price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery)
                        rows = mycursor.fetchall()
                elif(self.var_sort_dropdown.get() == "Low Price"):
                    print("Order BY price ASC")
                    sort_asc = " ORDER BY price ASC"
                    # no range
                    if(self.var_start_price.get() == "" and self.var_end_price.get() == ""):
                        print("No range")
                        mycursor.execute(query1+establishment_id_condition+"item_id IN "+subquery+sort_asc)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() != "" and self.var_end_price.get() == ""):
                        print("Start range.")
                        mycursor.execute(query1+establishment_id_condition+"price >= "+str(self.var_start_price.get())+" AND item_id IN "+subquery+sort_asc)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() == "" and self.var_end_price.get() != ""):
                        print("End range.")
                        mycursor.execute(query1+establishment_id_condition+"price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery+sort_asc)
                        rows = mycursor.fetchall()
                    else:
                        print("Start and End range.")
                        mycursor.execute(query1+establishment_id_condition+"price >= "+str(self.var_start_price.get())+" AND price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery+sort_asc)
                        rows = mycursor.fetchall()
                else:
                    print("Order BY price ASC")
                    sort_desc = " ORDER BY price DESC"
                    # no range
                    if(self.var_start_price.get() == "" and self.var_end_price.get() == ""):
                        print("No range")
                        mycursor.execute(query1+establishment_id_condition+"item_id IN "+subquery+sort_desc)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() != "" and self.var_end_price.get() == ""):
                        print("Start range.")
                        mycursor.execute(query1+establishment_id_condition+"price >= "+str(self.var_start_price.get())+" AND item_id IN "+subquery+sort_desc)
                        rows = mycursor.fetchall()
                    elif(self.var_start_price.get() == "" and self.var_end_price.get() != ""):
                        print("End range.")
                        mycursor.execute(query1+establishment_id_condition+"price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery+sort_desc)
                        rows = mycursor.fetchall()
                    else:
                        print("Start and End range.")
                        mycursor.execute(query1+establishment_id_condition+"price >= "+str(self.var_start_price.get())+" AND price <= "+str(self.var_end_price.get())+" AND item_id IN "+subquery+sort_desc)
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
        

if __name__ == "__main__":
    root=Tk()
    obj = FoodItemWindow(root)
    root.mainloop()