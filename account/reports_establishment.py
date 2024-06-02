from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

class EstablishmentWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Establishments")
        self.root.geometry("1100x550+0+90")
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        
        # title
        title_label = Label(self.root, text="Establishment Details", font=('Courier', 25, 'bold'), bg="#FFBA00", fg="#302400")
        title_label.pack(fill="x")  
        
        # right-side
        frame_label_right =LabelFrame(self.root, bd=2, relief=RIDGE, text="View Establishment Details", font=('Courier', 15, 'bold'), padx=2, bg="white")
        frame_label_right.place(x=0, y=45, width=1100, height=500)
        
        # filter label
        filter_label = Label(frame_label_right, text="Filter:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#302400")
        filter_label.grid(row=0, column=0, sticky=W, padx=2)
        
        # drop down filter
        self.var_filter_dropdown = StringVar()
        filter_search = ttk.Combobox(frame_label_right, font=('Courier', 12, 'bold'), width=15, state="readonly", textvariable=self.var_filter_dropdown)
        filter_search["value"] = ("", "High Rating", "Low Rating")
        filter_search.current(0)
        filter_search.grid(row=0, column=1, padx=5)
        
        
        # search label
        search_label = Label(frame_label_right, text="Search By:", font=('Courier', 12, 'bold'), bg="#FFBA00", fg="#302400")
        search_label.grid(row=0, column=2, sticky=W, padx=2)
        
        # drop down
        self.var_search = StringVar()
        select_search = ttk.Combobox(frame_label_right, font=('Courier', 12, 'bold'), width=15, state="readonly", textvariable=self.var_search)
        select_search["value"] = ("name", "location")
        select_search.current(0)
        select_search.grid(row=0, column=3)
        
        
        self.var_search_text = StringVar()
        search_entry = ttk.Entry(frame_label_right, font=('Courier', 12, 'bold'), width=20, textvariable=self.var_search_text)
        search_entry.grid(row=0, column=4, padx=2)
        
        # search button
        search_btn = Button(frame_label_right, text="Search", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#302400", activeforeground="white", cursor="hand2", width=10, command=self.search)
        search_btn.grid(row=0, column=5, padx=5)
        
        # show all button
        show_btn = Button(frame_label_right, text="Show All", font=('Courier', 12, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFA500", fg="#302400", activeforeground="white", cursor="hand2", width=10, command=self.fetch_data)
        show_btn.grid(row=0, column=6, padx=1)

        # ====================== results ======================
        data_frame = Frame(frame_label_right, relief=RIDGE)
        data_frame.place(x=0, y=70, width=1090, height=400)
        
        scroll_x = ttk.Scrollbar(data_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(data_frame, orient=VERTICAL)
        
        self.Establishment_Table = ttk.Treeview(data_frame, column=("establishment_id", "location", "description", "average_rating", "name"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
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
        self.fetch_data()

    # ====================== back end ======================
    # show data
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
    
    def search(self):
        try:
            mydb = mysql.connector.connect(host='localhost', user='root', password='server', database='project')
            mycursor = mydb.cursor()
                
            print("Connected to database...")
            
            if(str(self.var_filter_dropdown.get()) == "High Rating"):
                mycursor.execute("SELECT * FROM food_establishment where average_rating >= 4 and "+str(self.var_search.get())+" LIKE '%"+str(self.var_search_text.get())+"%'")
                rows = mycursor.fetchall()
                print("Query1")
            
            elif(str(self.var_filter_dropdown.get()) == "Low Rating"):
                mycursor.execute("SELECT * FROM food_establishment where average_rating < 4 and "+str(self.var_search.get())+" LIKE '%"+str(self.var_search_text.get())+"%'")
                rows = mycursor.fetchall()
                print("Query2")
            
            else:
                mycursor.execute("SELECT * FROM food_establishment where "+str(self.var_search.get())+" LIKE '%"+str(self.var_search_text.get())+"%'")
                rows = mycursor.fetchall()
                print("Query3")
                
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
        

if __name__ == "__main__":
    root=Tk()
    obj = EstablishmentWindow(root)
    root.mainloop()