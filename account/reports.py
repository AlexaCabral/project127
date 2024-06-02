from tkinter import *
from reports_establishment import EstablishmentWindow
from reports_food_item import FoodItemWindow
from reports_reviews import ReviewWindow

class MainSystem:
    def __init__(self, root):
       self.root = root
       self.root.title("System")
       self.root.geometry("1100x650+0+0")
       self.root.resizable(False, False)
       self.root.configure(bg="white")
       
       # frame
       navbar = Frame(self.root, bg="#FFBA00", height=50)
       navbar.pack(side="top", fill="x")
       
       # title
       title_label = Label(navbar, text="AnonameSystem", font=('Courier', 25, 'bold'), bg="#FFBA00", fg="#725B32")
       title_label.pack(side="left", padx=10, pady=10)
       
       # buttons
       establishment_btn= Button(navbar, text="Establishments", font=('Courier', 13, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFBA00", fg="#725B32", activeforeground="white", cursor="hand2", command=self.establishment_detail)
       
       review_btn = Button(navbar, text="Reviews", font=('Courier', 13, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFBA00", fg="#725B32", activeforeground="white", cursor="hand2", command=self.review_detail)
       
       food_items_btn = Button(navbar, text="Food Items", font=('Courier', 13, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFBA00", fg="#725B32", activeforeground="white", cursor="hand2", command=self.food_item_detail)
       
       logout_btn = Button(navbar, text="Logout", font=('Courier', 13, 'bold'), bd=0, bg="#FFBA00", activebackground="#FFBA00", fg="#725B32", activeforeground="white", cursor="hand2")
       
       # button placements
       logout_btn.pack(side="right", padx=10, pady=10)
       food_items_btn.pack(side="right", padx=10, pady=10)
       review_btn.pack(side="right", padx=10, pady=10)
       establishment_btn.pack(side="right", padx=10, pady=10)

       # Big text
       no_activity = Label(self.root, text="Get started.", font=('Courier', 60, 'bold'), bg="white", fg="#dedede", pady=200)
       no_activity.pack(fill=BOTH)
       
    
    def establishment_detail(self):
        self.new_window = Toplevel(self.root)
        self.app = EstablishmentWindow(self.new_window)
    
    def food_item_detail(self):
        self.new_window = Toplevel(self.root)
        self.app = FoodItemWindow(self.new_window)
    
    def review_detail(self):
        self.new_window = Toplevel(self.root)
        self.app = ReviewWindow(self.new_window)
       
# main window
if __name__ == "__main__":
    root = Tk()
    obj = MainSystem(root)
    root.mainloop()