"""This module provides a Tkinter application for a Party Hire Shop."""

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Constants
DROPDOWN_BG = "#68517B"
MAIN_BG = "#FDE992"
MAIN_FG = "#000000"
BUTTON_BG = "#6F2DA8"
BUTTON_FG = "#FFFFFF"
TEXT_BG = "#FFFFFF"
TEXT_FG = "#000000"
TEXT_FONT = ("Lexend", 11, "bold")
BUTTON_FONT = ("Lexend", 11, "bold")
ITEM_AMOUNT_LIMIT = 500
NAME_LENGTH_LIMIT = 100
MAX_RECEIPT_NUMBER = 9999999999
DATA_FILE = "party_hire_data.csv"

ITEMS = [
    "Party Hat", "Bouncy Castle", "Table", "Chair", "Cake",
    "Plate", "Fork", "Knife", "Pinata & Bat",
]


class MainApp:
    """The main GUI application class for managing party hires."""

    def __init__(self, root):
        """Initialize the application layout"""
        self.root = root
        self.root.title("Party Hire Store")
        try:
            self.root.iconbitmap("favicon.ico")
        except Exception:
            pass

        self.root.geometry("500x850")
        # change resizable to (false, false) to disable it on both axis
        self.root.resizable(True, True)
        self.root.configure(bg=MAIN_BG)
        
        self.style = ttk.Style()
        self.theme = self.style.theme_use("clam")
        
        self.style.configure(
            "Treeview",
            background=TEXT_BG,
            foreground=TEXT_FG,
            fieldbackground=TEXT_BG,
            rowheight=25,
            font=("Lexend", 10, "bold")
        )
        self.style.configure(
            "Treeview.Heading",
            background=BUTTON_BG,
            foreground=BUTTON_FG,
            font=("Lexend", 10, "bold")
        )
       
        self.style.map(
            "Treeview",
            background=[("selected", DROPDOWN_BG)],
            foreground=[("selected", MAIN_BG)]
        )

        self.hired_data = []
        self.load_data()
        self.create_widgets()
        self.update_treeview()
        self.root.after(100, self.show_welcome_message)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Create and arrange all visual elements in the application."""
        # Title
        self.title_label = tk.Label(
            self.root, text="🎉 Party Hire Store 🎉",
            bg=MAIN_BG, fg=MAIN_FG, font=("Lexend", 20, "bold")
        )
        self.title_label.pack(pady=15)

        # Name
        self.first_name_label = tk.Label(
            self.root, text="First Name:",
            bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT
        )
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(
            self.root, bg=TEXT_BG, fg=TEXT_FG,
            font=TEXT_FONT, relief=tk.SOLID, bd=1
        )
        self.first_name_entry.pack(pady=5, ipady=3)
        self.first_name_entry.bind('<Return>', self.handle_submit)

        self.last_name_label = tk.Label(
            self.root, text="Last Name:",
            bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT
        )
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(
            self.root, bg=TEXT_BG, fg=TEXT_FG,
            font=TEXT_FONT, relief=tk.SOLID, bd=1
        )
        self.last_name_entry.pack(pady=5, ipady=3)
        self.last_name_entry.bind('<Return>', self.handle_submit)

        self.receipt_label = tk.Label(
            self.root, text="Receipt Number:",
            bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT
        )
        self.receipt_label.pack()
        self.receipt_entry = tk.Entry(
            self.root, bg=TEXT_BG, fg=TEXT_FG,
            font=TEXT_FONT, relief=tk.SOLID, bd=1
        )
        self.receipt_entry.pack(pady=5, ipady=3)
        self.receipt_entry.bind('<Return>', self.handle_submit)

        # Dropdown
        self.selected = tk.StringVar(self.root)
        self.selected.set("Choose an item")

        dropdown = tk.OptionMenu(self.root, self.selected, *ITEMS)
        dropdown.config(
            bg=TEXT_BG, fg=TEXT_FG, activebackground=TEXT_BG,
            activeforeground=TEXT_FG, relief=tk.SOLID, bd=1
        )
        dropdown["menu"].config(
            bg=DROPDOWN_BG, fg=MAIN_BG,
            activebackground=BUTTON_BG,
            activeforeground=TEXT_BG
        )
        dropdown.pack(pady=10)

        # Item Amount
        self.item_amount_label = tk.Label(
            self.root, text="Amount of Items:",
            bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT
        )
        self.item_amount_label.pack()
        self.item_amount_entry = tk.Entry(
            self.root, bg=TEXT_BG, fg=TEXT_FG,
            font=TEXT_FONT, relief=tk.SOLID, bd=1
        )
        self.item_amount_entry.pack(pady=5, ipady=3)
        self.item_amount_entry.bind('<Return>', self.handle_submit)

        # Submit
        self.submit_button = tk.Button(
            self.root, text="Submit",
            command=self.handle_submit,
            bg=BUTTON_BG, fg=BUTTON_FG,
            font=BUTTON_FONT, cursor="hand1",
            relief=tk.GROOVE, bd=2
        )
        self.submit_button.pack(pady=10, ipadx=10)

        # Current Hires Header
        tk.Label(
            self.root,
            text="Current Hires (Click hire to select for return):",
            bg=MAIN_BG, fg=MAIN_FG,
            font=("Lexend", 10, "bold")
        ).pack(pady=5)

        # Treeview Config
        tree_frame = tk.Frame(self.root, bg=MAIN_BG)
        tree_frame.pack(pady=5, padx=10)

        columns = ('receipt', 'name', 'item', 'amount')
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show='headings', height=8
        )

        self.tree.heading('receipt', text='Receipt')
        self.tree.heading('name', text='Name')
        self.tree.heading('item', text='Item')
        self.tree.heading('amount', text='Qty')

        self.tree.column('receipt', width=100, anchor=tk.CENTER)
        self.tree.column('name', width=140, anchor=tk.W)
        self.tree.column('item', width=120, anchor=tk.W)
        self.tree.column('amount', width=50, anchor=tk.CENTER)

        # Treeview Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Return Item
        tk.Label(
            self.root, text="Return by Receipt Number:",
            bg=MAIN_BG, fg=MAIN_FG, font=TEXT_FONT
        ).pack(pady=(10, 0))
        self.remove_item_entry = tk.Entry(
            self.root, bg=TEXT_BG, fg=TEXT_FG,
            font=TEXT_FONT, relief=tk.SOLID, bd=1
        )
        self.remove_item_entry.pack(pady=5, ipady=3)
        self.remove_item_entry.bind('<Return>', self.handle_delete)

        self.remove_item_button = tk.Button(
            self.root, text="Return Item",
            command=self.handle_delete,
            bg=BUTTON_BG, fg=BUTTON_FG,
            font=BUTTON_FONT, cursor="hand1",
            relief=tk.GROOVE, bd=2
        )
        self.remove_item_button.pack(pady=5, ipadx=10)

    def load_data(self):
        """Load data safely from the CSV file into memory using comprehensive list validation."""
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            self.hired_data = []
            return

        try:
            with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                required_fields = ['receipt', 'name', 'item', 'amount']
                
                if reader.fieldnames and all(field in reader.fieldnames for field in required_fields):
                    self.hired_data = [
                        {
                            'receipt': int(row['receipt']),
                            'name': row['name'],
                            'item': row['item'],
                            'amount': int(row['amount']),
                        }
                        for row in reader
                        if all(row.get(f) is not None for f in required_fields)
                    ]
                else:
                    self.hired_data = []
        except (ValueError, KeyError, IOError):
            self.hired_data = []

    def save_data(self):
        """Save memory-cached hire data to the CSV file."""
        try:
            with open(DATA_FILE, mode='w', newline='',
                      encoding='utf-8') as file:
                fieldnames = ['receipt', 'name', 'item', 'amount']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.hired_data)
            return True
        except IOError as e:
            messagebox.showerror(
                "File Error",
                f"Could not save data to database.\nReason: {e}"
            )
            return False

    def update_treeview(self):
        """Refresh the UI Treeview element with current data."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Sort hires by name safely
        sorted_hires = sorted(
            self.hired_data,
            key=lambda hire: hire["name"].lower()
        )

        for hire in sorted_hires:
            self.tree.insert(
                '', tk.END,
                values=(
                    hire['receipt'], hire['name'],
                    hire['item'], hire['amount']
                )
            )

    def on_tree_select(self, event):
        """Populate the removal box safely, ensuring elements exist."""
        selection = self.tree.selection()
        if not selection:
            return

        item_info = self.tree.item(selection[0])
        item_data = item_info.get('values')
        
        if item_data and len(item_data) > 0:
            self.remove_item_entry.delete(0, tk.END)
            self.remove_item_entry.insert(0, str(item_data[0]))

    def clear_form(self):
        """Reset inputs and selection models to default states."""
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.receipt_entry.delete(0, tk.END)
        self.item_amount_entry.delete(0, tk.END)
        self.remove_item_entry.delete(0, tk.END)
        self.selected.set("Choose an item")

    def handle_submit(self, event=None):
        """Validate input data and commit a new hire receipt."""
        first_name = self.first_name_entry.get().strip().capitalize()
        last_name = self.last_name_entry.get().strip().capitalize()
        item_amount_raw = self.item_amount_entry.get().strip()
        option = self.selected.get().strip()
        receipt_input = self.receipt_entry.get().strip()

        if not first_name or not last_name or not item_amount_raw or option == "Choose an item" or not receipt_input:
            messagebox.showwarning(
                "Uh Oh!",
                "Please complete all fields before submitting."
            )
            return
        elif len(first_name) > NAME_LENGTH_LIMIT or len(last_name) > NAME_LENGTH_LIMIT:
            messagebox.showwarning(
                "Uh Oh!",
                f"Name exceeds limit (Max {NAME_LENGTH_LIMIT} characters)."
            )
            return
        elif not item_amount_raw.isdigit() or int(item_amount_raw) <= 0:
            messagebox.showwarning(
                "Uh Oh!",
                "Amount must be a positive whole number."
            )
            return
        elif not receipt_input.isdigit() or int(receipt_input) <= 0:
            messagebox.showwarning(
                "Uh Oh!",
                "Receipt number must be a positive whole number."
            )
            return
        elif int(receipt_input) > MAX_RECEIPT_NUMBER:
            messagebox.showwarning(
                "Uh Oh!",
                f"Receipt number exceeds maximum allowed value ({MAX_RECEIPT_NUMBER})."
            )
            return

        item_amount = int(item_amount_raw)
        if item_amount > ITEM_AMOUNT_LIMIT:
            messagebox.showwarning(
                "Uh Oh!",
                f"Amount cannot exceed {ITEM_AMOUNT_LIMIT} units."
            )
            return

        receipt = int(receipt_input)
        if any(hire['receipt'] == receipt for hire in self.hired_data):
            messagebox.showwarning(
                "Uh Oh!",
                "receipt number already in use."
            )
            return

        # Combines first and last name
        full_name = f"{first_name} {last_name}"

        self.hired_data.append({
            'receipt': receipt, 'name': full_name,
            'item': option, 'amount': item_amount
        })

        if self.save_data():
            self.update_treeview()
            self.clear_form()
            messagebox.showinfo(
                "Success",
                f"Successfully hired {option} (x{item_amount}).\n"
                f"Receipt Number: {receipt}"
            )

    def handle_delete(self, event=None):
        """Remove a hire item by targeting its receipt number."""
        receipt_to_remove = self.remove_item_entry.get().strip()
        if not receipt_to_remove.isdigit():
            messagebox.showwarning(
                "Error",
                "Please enter a valid numeric receipt number."
            )
            return

        receipt_int = int(receipt_to_remove)
        target_item = next(
            (h for h in self.hired_data if h['receipt'] == receipt_int),
            None
        )

        if target_item is None:
            messagebox.showwarning(
                "Not Found",
                "The provided receipt number could not be found."
            )
        else:
            current_selection = self.tree.selection()
            if current_selection:
                self.tree.selection_remove(current_selection)

            self.hired_data.remove(target_item)

            if self.save_data():
                self.update_treeview()
                self.clear_form()
                messagebox.showinfo(
                    "Success",
                    "Item has been successfully returned."
                )
            else:
                self.hired_data.append(target_item)

    def show_welcome_message(self):
        """Display a greeting popup shortly after startup."""
        messagebox.showinfo(
            "Welcome",
            "Welcome to the Party Hire Store.\n"
            "Use the interface to take out or return hires."
        )

    def on_closing(self):
        """Intercept application close to prompt for confirmation."""
        if messagebox.askokcancel(
            "Exit Application",
            "Are you sure you want to exit?"
        ):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()