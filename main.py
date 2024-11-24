import tkinter as tk  # tkinter library for GUI creation
from tkinter import ttk, messagebox, simpledialog  #  specific modules for widgets, dialogs, and messages
import json  # JSON module for reading and writing data
from PIL import Image, ImageTk  # Import PIL for handling images
from ttkbootstrap import Style, ttk  #  ttkbootstrap for styled widgets
from ttkbootstrap.constants import *  #  constants for ttkbootstrap styles

# responsible for managing personal finance transactions
class PersonalFinanceManager:
    def __init__(self, username):
        self.username = username
        self.transactions = []
        self.load_transactions()

    # Load transactions from a JSON file
    def load_transactions(self):
        try:
            with open(f'{self.username}_transactions.json', 'r') as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = []

    # Save transactions to a JSON file
    def save_transactions(self):
        with open(f'{self.username}_transactions.json', 'w') as file:
            json.dump(self.transactions, file)

    # add a transaction (income/expense) to the list
    def add_transaction(self, transaction_type, amount, description):
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "description": description
        }
        self.transactions.append(transaction)
        self.save_transactions()

    # delete transac with index
    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            self.save_transactions()

    # getting the overall summary
    def get_summary(self):
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        balance = total_income - total_expenses
        return total_income, total_expenses, balance
    
# Main class for the GUI
class FinanceWiseApp:
    def __init__(self, root, image_path="1.png"):
        self.root = root
        self.root.title("FinanceWise")
        self.root.geometry("850x500")
        self.root.configure(bg="white")
        self.finance_manager = None
        self.canvas = None

        #  ttkbootstrap style
        self.style = Style(theme="flatly")  

        
        self.style.configure(
            "BlackButton.TButton",
            background="gray",
            foreground="black",
            borderwidth=2,
            relief="flat",
            padding=(10, 5),
            font=("nacelle", 12, "bold")  

        )

        self.style.map(
            "BlackButton.TButton",
            background=[("active", "black"), ("hover", "black")],  
            foreground=[("active", "gray"), ("hover", "red")]  
        )

        # Set up the login screen
        self.setup_login_screen(image_path)

    def setup_background(self, image_path):
        try:
            # load the image
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((850, 500))  # size to fit the window
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            # Create a canvas and set the image as the background
            self.canvas = tk.Canvas(self.root, width=600, height=400)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")
            messagebox.showerror("Error", f"Could not load image: {image_path}. Please check the file path.")
    # clear widgets from screen
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    # Set up the login screen with buttons for login and account creation
    def setup_login_screen(self, image_path):
        self.clear_screen()
        self.setup_background(image_path)

        #create acc button
        ttk.Button(
            self.root,
            text="Create Account",
            style="BlackButton.TButton",  
            command=self.create_account_screen
        ).place(x=615, y=275, width=185)
        #login button
        ttk.Button(
            self.root,
            text="Login",
            style="BlackButton.TButton", 
            command=self.login_screen
        ).place(x=615, y=330, width=185)


    def create_account_screen(self):
        self.clear_screen()
        self.setup_background("kreyt.png")  


        # Username label and entry
        self.username_entry = ttk.Entry(self.root, font=("poppins", 12))
        self.username_entry.place(x=333, y=195, width=200)

        # Password label and entry
        self.password_entry = ttk.Entry(self.root, font=("poppins", 12), show="*")
        self.password_entry.place(x=333, y=249, width=200)

        # Re-enter Password label and entry
        self.reenter_password_entry = ttk.Entry(self.root, font=("Poppins", 12), show="*")  # Re-enter password field
        self.reenter_password_entry.place(x=333, y=302, width=200)

        ttk.Button(
        self.root,
        text="Create",  # Button label "Create"
        style="BlackButton.TButton",  
        command=self.create_account  # function for creating account
        ).place(x=330, y=350, width=100)

        #  Back button 
        ttk.Button(
        self.root,
        text="Back",  # Button label "Back"
        style="BlackButton.TButton",  
        command=lambda: self.setup_login_screen("1.png")).place(x=435, y=350, width=100)

    # creating an account
    def create_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        reenter_password = self.reenter_password_entry.get()


        if not username or not password or not reenter_password:
            messagebox.showerror("Error", "Please fill in all fields.") # checks if fields are empty
            return

        if password != reenter_password:
         messagebox.showerror("Error", "Passwords do not match. Please try again.") # checks if the password match
         return

        try:
            with open('accounts.json', 'r') as file:
                accounts = json.load(file) #load existing accounts
        except FileNotFoundError:
            accounts = {}

        if username in accounts:
            messagebox.showerror("Error", "Username already exists!") # checks if the username already exists
            return

        accounts[username] = password # saved to accounts.json
        with open('accounts.json', 'w') as file:
            json.dump(accounts, file)

        messagebox.showinfo("Success", "Account created successfully!")
        self.setup_login_screen("1.png") # return to login screen

    # login window
    def login_screen(self):
        
        self.clear_screen()
        self.setup_background("lag.png")  

        self.username_entry = ttk.Entry(self.root, font=("work sans", 12))
        self.username_entry.place(x=333, y=195, width=200)

        self.password_entry = ttk.Entry(self.root, font=("work sans", 12), show="*")
        self.password_entry.place(x=333, y=249, width=200)

        style = ttk.Style()

        style.configure("BlackButton.TButton",
            background="gray",  
            foreground="white",    
            font=("Poppins", 12, "bold"),  
            padding=10,  
            relief="flat")  
        style.map("BlackButton.TButton",
            background=[('active', 'black')],  
            foreground=[('active', 'white')])     

        # login button  custom 
        ttk.Button(self.root, 
            text="Login", 
            style="BlackButton.TButton",  
            command=self.login).place(x=319, y=305, width=100)

        # back button
        ttk.Button(self.root, 
            text="Back", 
            style="BlackButton.TButton",  # application of custom style
            command=lambda: self.setup_login_screen("1.png")).place(x=430, y=305, width=100)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            with open('accounts.json', 'r') as file: #Checks if the provided credentials exist in the accounts.json file.
                accounts = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "No accounts found. Please create an account.")
            return

        if username in accounts and accounts[username] == password: #If credentials are valid, transitions to the dashboard screen
            self.finance_manager = PersonalFinanceManager(username)
            self.dashboard_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def dashboard_screen(self):
        self.clear_screen()
        self.setup_background("menu1.png")  

    # Welcome back message
        welcome_message = f"Welcome back, {self.finance_manager.username.capitalize()}!"
        ttk.Label(self.root, text=welcome_message, font=("arial", 12, "bold")).place(x=323, y=59)

        ttk.Button(
        self.root,
        text="Add Income",
        style="BlackButton.TButton",  # Apply the custom style
        command=lambda: self.add_transaction_screen('income')).place(x=325, y=170, width=200)

    # Add Expense Button
        ttk.Button(
        self.root,
        text="Add Expense",
        style="BlackButton.TButton",  # Apply the custom style
        command=lambda: self.add_transaction_screen('expense')).place(x=325, y=220, width=200)
    # View Transactions Button
        ttk.Button(
        self.root,
        text="View Transactions",
        style="BlackButton.TButton",  # Apply the custom style
        command=self.view_transactions).place(x=325, y=270, width=200)

    # Delete Transactions Button
        ttk.Button(
        self.root,
        text="Delete Transactions",
        style="BlackButton.TButton",  # Apply the custom style
        command=self.delete_transaction_screen).place(x=325, y=320, width=200)

    # View Summary Button
        ttk.Button(
        self.root,
        text="View Summary",
        style="BlackButton.TButton",  # Apply the custom style
        command=self.view_summary).place(x=325, y=370, width=200)

    # Logout Button
        ttk.Button(
        self.root,
        text="Logout",
        style="BlackButton.TButton",  # Apply the custom style
        command=self.logout).place(x=325, y=420, width=200)

    def add_transaction_screen(self, transaction_type):
        amount = simpledialog.askfloat("Transaction", f"Enter {transaction_type} amount:")
        if amount is None:
            return
        description = simpledialog.askstring("Transaction", "Enter description:")
        if description is None:
            return

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than zero.")
            return

        self.finance_manager.add_transaction(transaction_type, amount, description)
        messagebox.showinfo("Success", f"{transaction_type.capitalize()} added successfully!")
        self.dashboard_screen()

    def view_transactions(self):
        transactions_window = tk.Toplevel(self.root)
        transactions_window.title("Transactions")
        transactions_window.geometry("600x400")
        transactions_window.configure(bg="black")

        listbox = tk.Listbox(transactions_window, font=("arial", 12, "bold"), height=15, width=50)
        listbox.pack(pady=5)

        for idx, transaction in enumerate(self.finance_manager.transactions, start=1):
            listbox.insert(
                tk.END,
                f"{idx}. {transaction['type'].capitalize()}: ${transaction['amount']:.2f} - {transaction['description']}"
            )

        ttk.Button(
        transactions_window,
        text="Close",
        style="BlackButton.TButton",  # Apply custom style
        command=transactions_window.destroy
    ).pack(pady=10)


    def delete_transaction_screen(self):
        if not self.finance_manager.transactions:
            messagebox.showinfo("Delete", "No transactions found.")
            return
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Transaction")
        delete_window.geometry("600x480")
        delete_window.configure(bg="black")

        listbox = tk.Listbox(delete_window, font=("arial", 12, "bold"), height=15, width=50)
        listbox.pack(pady=10)

        for idx, transaction in enumerate(self.finance_manager.transactions, start=1):
            listbox.insert(
                tk.END,
                f"{idx}. {transaction['type'].capitalize()}: ${transaction['amount']:.2f} - {transaction['description']}"
            )

        def delete_selected():
            try:
                selected_index = listbox.curselection()[0]
                self.finance_manager.delete_transaction(selected_index)
                delete_window.destroy()
                self.dashboard_screen()
            except IndexError:
                messagebox.showwarning("Warning", "Please select a transaction to delete.")
        
        ttk.Button(
        delete_window,
        text="Delete",
        style="BlackButton.TButton",  # Apply custom style
        command=delete_selected
    ).pack(pady=10)

    # Styled "Close" button
        ttk.Button(
        delete_window,
        text="Close",
        style="BlackButton.TButton",  # Apply custom style
        command=delete_window.destroy
    ).pack(pady=10)

    def view_summary(self):
        total_income, total_expenses, balance = self.finance_manager.get_summary()
        summary = (
            f"Total Income: ${total_income:.2f}\n"
            f"Total Expenses: ${total_expenses:.2f}\n"
            f"Balance: ${balance:.2f}"
        )
        messagebox.showinfo("Summary", summary)
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def logout(self):
    # Clear the current screen and show the login screen
     self.clear_screen()
     self.setup_login_screen("1.png")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceWiseApp(root, image_path="1.png")
    root.mainloop()
