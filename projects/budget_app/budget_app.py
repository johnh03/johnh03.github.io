import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "budget_data.json"

CATEGORIES = [
    "Rent", "Utilities", "Groceries",
    "Entertainment", "Gas",
    "Credit Card", "Other"
]

PAYMENT_METHODS = ["Cash", "Debit", "Credit"]

# Modern color scheme
COLORS = {
    "bg_primary": "#0f172a",      # Dark navy
    "bg_secondary": "#1e293b",    # Darker slate
    "accent": "#3b82f6",          # Blue
    "accent_light": "#60a5fa",    # Light blue
    "success": "#10b981",         # Green
    "warning": "#f59e0b",         # Amber
    "danger": "#ef4444",          # Red
    "text_primary": "#f1f5f9",    # Light text
    "text_secondary": "#cbd5e1",  # Medium text
    "border": "#334155"           # Border color
}


# --------------------------
# Data Handling
# --------------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --------------------------
# App
# --------------------------

class BudgetApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("750x700")
        self.root.resizable(False, False)
        
        # Set dark theme
        self.root.configure(bg=COLORS["bg_primary"])

        self.data = load_data()
        self.current_month = tk.StringVar()
        self.months = self.generate_months()
        self.current_month.set(self.months[0])

        self.setup_styles()
        self.create_widgets()
        self.update_summary()

    def generate_months(self):
        months = []
        now = datetime.now()
        for i in range(12):
            month = datetime(now.year, i+1, 1).strftime("%B %Y")
            months.append(month)
        return months

    def ensure_month_exists(self):
        month = self.current_month.get()
        if month not in self.data:
            self.data[month] = {
                "income": 0,
                "expenses": [],
                "budget": 0
            }

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for different elements
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), foreground=COLORS["text_primary"])
        style.configure('TLabel', background=COLORS["bg_primary"], foreground=COLORS["text_primary"], font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=COLORS["bg_primary"], foreground=COLORS["accent_light"], font=('Segoe UI', 20, 'bold'))
        style.configure('Subtitle.TLabel', background=COLORS["bg_secondary"], foreground=COLORS["text_secondary"], font=('Segoe UI', 9))
        style.configure('TCombobox', font=('Segoe UI', 10))
        
        # Style the Combobox
        style.configure('TCombobox', fieldbackground=COLORS["bg_secondary"], background=COLORS["bg_secondary"], foreground=COLORS["text_primary"])

    # --------------------------
    # UI
    # --------------------------

    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=COLORS["bg_primary"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(header_frame, text="💰 Budget Tracker", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)

        # Month Selection Frame
        month_frame = tk.Frame(main_frame, bg=COLORS["bg_secondary"], highlightthickness=1, highlightbackground=COLORS["border"])
        month_frame.pack(fill=tk.X, pady=(0, 20), padx=0)
        month_frame.pack_propagate(False)
        month_frame.configure(height=60)

        month_label = ttk.Label(month_frame, text="Select Month:", style='Subtitle.TLabel')
        month_label.pack(side=tk.LEFT, padx=15, pady=10)

        month_dropdown = ttk.Combobox(
            month_frame,
            textvariable=self.current_month,
            values=self.months,
            width=20,
            state='readonly'
        )
        month_dropdown.pack(side=tk.LEFT, padx=5, pady=10)
        month_dropdown.configure(foreground=COLORS["text_primary"])
        month_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_summary())

        # Summary Cards Frame
        summary_container = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        summary_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Income Card
        income_card = tk.Frame(summary_container, bg=COLORS["bg_secondary"], highlightthickness=1, highlightbackground=COLORS["success"])
        income_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        ttk.Label(income_card, text="Income", style='Subtitle.TLabel').pack(pady=(15, 5), padx=15)
        self.income_label = tk.Label(
            income_card, 
            text="$0.00", 
            font=('Segoe UI', 24, 'bold'),
            fg=COLORS["success"],
            bg=COLORS["bg_secondary"]
        )
        self.income_label.pack(pady=(0, 15), padx=15)

        # Expenses Card
        expenses_card = tk.Frame(summary_container, bg=COLORS["bg_secondary"], highlightthickness=1, highlightbackground=COLORS["danger"])
        expenses_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(expenses_card, text="Expenses", style='Subtitle.TLabel').pack(pady=(15, 5), padx=15)
        self.expenses_label = tk.Label(
            expenses_card, 
            text="$0.00", 
            font=('Segoe UI', 24, 'bold'),
            fg=COLORS["danger"],
            bg=COLORS["bg_secondary"]
        )
        self.expenses_label.pack(pady=(0, 15), padx=15)

        # Budget Card
        budget_card = tk.Frame(summary_container, bg=COLORS["bg_secondary"], highlightthickness=1, highlightbackground=COLORS["warning"])
        budget_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        ttk.Label(budget_card, text="Budget", style='Subtitle.TLabel').pack(pady=(15, 5), padx=15)
        self.budget_label = tk.Label(
            budget_card, 
            text="$0.00", 
            font=('Segoe UI', 24, 'bold'),
            fg=COLORS["warning"],
            bg=COLORS["bg_secondary"]
        )
        self.budget_label.pack(pady=(0, 15), padx=15)

        # Balance Card
        balance_card = tk.Frame(summary_container, bg=COLORS["bg_secondary"], highlightthickness=1, highlightbackground=COLORS["accent"])
        balance_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        ttk.Label(balance_card, text="Remaining", style='Subtitle.TLabel').pack(pady=(15, 5), padx=15)
        self.balance_label = tk.Label(
            balance_card, 
            text="$0.00", 
            font=('Segoe UI', 24, 'bold'),
            fg=COLORS["accent_light"],
            bg=COLORS["bg_secondary"]
        )
        self.balance_label.pack(pady=(0, 15), padx=15)

        # Transactions Frame
        transactions_label = ttk.Label(main_frame, text="Recent Transactions", style='Subtitle.TLabel')
        transactions_label.pack(fill=tk.X, pady=(20, 10))

        # Transactions List
        list_frame = tk.Frame(main_frame, bg=COLORS["bg_secondary"], highlightthickness=1, highlightbackground=COLORS["border"])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Scrollbar for transactions
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.transactions_text = scrolledtext.ScrolledText(
            list_frame,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 9),
            height=8,
            width=80,
            relief=tk.FLAT,
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set
        )
        self.transactions_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        scrollbar.config(command=self.transactions_text.yview)

        # Buttons Frame
        button_frame = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        button_frame.pack(fill=tk.X, pady=(0, 0))

        add_income_btn = tk.Button(
            button_frame,
            text="+ Add Income",
            command=self.add_income,
            bg=COLORS["success"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        add_income_btn.pack(side=tk.LEFT, padx=(0, 5), fill=tk.BOTH, expand=True)

        add_expense_btn = tk.Button(
            button_frame,
            text="+ Add Expense",
            command=self.add_expense,
            bg=COLORS["danger"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        add_expense_btn.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        chart_btn = tk.Button(
            button_frame,
            text="📊 Expenses Chart",
            command=self.show_pie_chart,
            bg=COLORS["accent"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        chart_btn.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        budget_btn = tk.Button(
            button_frame,
            text="💰 Set Budget",
            command=self.set_budget,
            bg=COLORS["warning"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        budget_btn.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        # Second row of buttons
        button_frame2 = tk.Frame(main_frame, bg=COLORS["bg_primary"])
        button_frame2.pack(fill=tk.X, pady=(10, 0))

        delete_btn = tk.Button(
            button_frame2,
            text="🗑️ Delete Expense",
            command=self.delete_expense,
            bg="#8b5cf6",
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=(0, 5), fill=tk.BOTH, expand=True)

        clear_month_btn = tk.Button(
            button_frame2,
            text="⚠️ Clear Month",
            command=self.clear_month,
            bg="#dc2626",
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        clear_month_btn.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

    # --------------------------
    # Features
    # --------------------------

    def add_income(self):
        self.ensure_month_exists()

        window = tk.Toplevel(self.root)
        window.title("Add Income")
        window.geometry("300x180")
        window.configure(bg=COLORS["bg_primary"])
        window.resizable(False, False)

        # Center the window
        window.transient(self.root)
        window.grab_set()

        frame = tk.Frame(window, bg=COLORS["bg_primary"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(frame, text="Income Amount:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        amount_var = tk.StringVar()
        amount_entry = tk.Entry(
            frame,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            insertbackground=COLORS["accent_light"],
            bd=1
        )
        amount_entry.pack(fill=tk.X, pady=(0, 20))
        amount_entry.focus()

        def submit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Invalid", "Amount must be positive", parent=window)
                    return
                
                self.data[self.current_month.get()]["income"] += amount
                save_data(self.data)
                self.update_summary()
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount", parent=window)

        button_frame = tk.Frame(frame, bg=COLORS["bg_primary"])
        button_frame.pack(fill=tk.X, pady=(10, 0))

        submit_btn = tk.Button(
            button_frame,
            text="Add Income",
            command=submit,
            bg=COLORS["success"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.RIGHT, padx=(5, 0))

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.RIGHT)

    def add_expense(self):
        self.ensure_month_exists()

        window = tk.Toplevel(self.root)
        window.title("Add Expense")
        window.geometry("350x350")
        window.configure(bg=COLORS["bg_primary"])
        window.resizable(False, False)

        # Center the window
        window.transient(self.root)
        window.grab_set()

        frame = tk.Frame(window, bg=COLORS["bg_primary"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Amount
        ttk.Label(frame, text="Amount:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        amount_entry = tk.Entry(
            frame,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            insertbackground=COLORS["accent_light"],
            bd=1
        )
        amount_entry.pack(fill=tk.X, pady=(0, 15))

        # Category
        ttk.Label(frame, text="Category:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            frame,
            textvariable=category_var,
            values=CATEGORIES,
            state='readonly',
            width=30
        )
        category_combo.pack(fill=tk.X, pady=(0, 15))

        # Payment Method
        ttk.Label(frame, text="Payment Method:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        payment_var = tk.StringVar()
        payment_combo = ttk.Combobox(
            frame,
            textvariable=payment_var,
            values=PAYMENT_METHODS,
            state='readonly',
            width=30
        )
        payment_combo.pack(fill=tk.X, pady=(0, 20))

        def submit():
            try:
                amount = float(amount_entry.get())
                category = category_var.get()
                payment = payment_var.get()

                if amount <= 0:
                    messagebox.showerror("Invalid", "Amount must be positive", parent=window)
                    return
                if not category:
                    messagebox.showerror("Invalid", "Please select a category", parent=window)
                    return
                if not payment:
                    messagebox.showerror("Invalid", "Please select a payment method", parent=window)
                    return

                self.data[self.current_month.get()]["expenses"].append({
                    "amount": amount,
                    "category": category,
                    "payment": payment,
                    "date": datetime.now().strftime("%m/%d/%y")
                })

                save_data(self.data)
                self.update_summary()
                window.destroy()

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount", parent=window)

        button_frame = tk.Frame(frame, bg=COLORS["bg_primary"])
        button_frame.pack(fill=tk.X, pady=(10, 0))

        submit_btn = tk.Button(
            button_frame,
            text="Add Expense",
            command=submit,
            bg=COLORS["danger"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.RIGHT, padx=(5, 0))

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.RIGHT)

    def update_summary(self):
        self.ensure_month_exists()

        month_data = self.data[self.current_month.get()]
        income = month_data["income"]
        expenses = sum(e["amount"] for e in month_data["expenses"])
        budget = month_data.get("budget", 0)
        balance = income - expenses

        # Update summary cards
        self.income_label.config(text=f"${income:.2f}")
        self.expenses_label.config(text=f"${expenses:.2f}")
        self.budget_label.config(text=f"${budget:.2f}")
        
        # Color balance based on positive/negative
        balance_color = COLORS["success"] if balance >= 0 else COLORS["danger"]
        self.balance_label.config(text=f"${balance:.2f}", fg=balance_color)

        # Update transactions list
        self.update_transactions_list()

    def update_transactions_list(self):
        """Display recent transactions in the text widget"""
        self.transactions_text.config(state=tk.NORMAL)
        self.transactions_text.delete(1.0, tk.END)

        month_data = self.data[self.current_month.get()]
        
        if not month_data["expenses"]:
            self.transactions_text.insert(tk.END, "No transactions yet", "center")
            self.transactions_text.config(state=tk.DISABLED)
            return

        # Configure text tags for styling
        self.transactions_text.tag_configure("header", foreground=COLORS["accent_light"], font=('Segoe UI', 9, 'bold'))
        self.transactions_text.tag_configure("category", foreground=COLORS["text_secondary"])
        self.transactions_text.tag_configure("amount", foreground=COLORS["danger"])

        # Display expenses
        for i, expense in enumerate(month_data["expenses"], 1):
            date = expense.get("date", "N/A")
            category = expense["category"]
            amount = expense["amount"]
            payment = expense["payment"]
            
            line = f"{i}. {category:<20} ${amount:>8.2f}  |  {payment:<8}  |  {date}\n"
            self.transactions_text.insert(tk.END, line)

        self.transactions_text.config(state=tk.DISABLED)

    def set_budget(self):
        """Set a budget limit for the current month"""
        self.ensure_month_exists()

        window = tk.Toplevel(self.root)
        window.title("Set Monthly Budget")
        window.geometry("300x180")
        window.configure(bg=COLORS["bg_primary"])
        window.resizable(False, False)

        window.transient(self.root)
        window.grab_set()

        frame = tk.Frame(window, bg=COLORS["bg_primary"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(frame, text="Monthly Budget Limit:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        budget_entry = tk.Entry(
            frame,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            insertbackground=COLORS["accent_light"],
            bd=1
        )
        budget_entry.pack(fill=tk.X, pady=(0, 20))
        budget_entry.insert(0, str(self.data[self.current_month.get()].get("budget", 0)))
        budget_entry.focus()

        def submit():
            try:
                budget = float(budget_entry.get())
                if budget < 0:
                    messagebox.showerror("Invalid", "Budget must be positive or zero", parent=window)
                    return
                
                self.data[self.current_month.get()]["budget"] = budget
                save_data(self.data)
                self.update_summary()
                messagebox.showinfo("Success", f"Budget set to ${budget:.2f}", parent=window)
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount", parent=window)

        button_frame = tk.Frame(frame, bg=COLORS["bg_primary"])
        button_frame.pack(fill=tk.X, pady=(10, 0))

        submit_btn = tk.Button(
            button_frame,
            text="Set Budget",
            command=submit,
            bg=COLORS["warning"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.RIGHT, padx=(5, 0))

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.RIGHT)

    def delete_expense(self):
        """Delete a specific expense from the current month"""
        self.ensure_month_exists()

        month_data = self.data[self.current_month.get()]
        if not month_data["expenses"]:
            messagebox.showinfo("No Data", "No expenses to delete")
            return

        window = tk.Toplevel(self.root)
        window.title("Delete Expense")
        window.geometry("400x300")
        window.configure(bg=COLORS["bg_primary"])
        window.resizable(False, False)

        window.transient(self.root)
        window.grab_set()

        frame = tk.Frame(window, bg=COLORS["bg_primary"])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(frame, text="Select expense to delete:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 10))

        # Create listbox with expenses
        listbox_frame = tk.Frame(frame, bg=COLORS["bg_secondary"], highlightthickness=1, highlightbackground=COLORS["border"])
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            listbox_frame,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10),
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            bd=0
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        scrollbar.config(command=listbox.yview)

        # Populate listbox
        for i, expense in enumerate(month_data["expenses"]):
            date = expense.get("date", "N/A")
            category = expense["category"]
            amount = expense["amount"]
            payment = expense["payment"]
            listbox.insert(tk.END, f"{category:<15} ${amount:>8.2f}  |  {payment:<8}  |  {date}")

        def delete():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an expense to delete", parent=window)
                return

            if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?", parent=window):
                idx = selection[0]
                del self.data[self.current_month.get()]["expenses"][idx]
                save_data(self.data)
                self.update_summary()
                window.destroy()

        button_frame = tk.Frame(frame, bg=COLORS["bg_primary"])
        button_frame.pack(fill=tk.X)

        delete_btn = tk.Button(
            button_frame,
            text="Delete",
            command=delete,
            bg=COLORS["danger"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        delete_btn.pack(side=tk.RIGHT, padx=(5, 0))

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.RIGHT)

    def clear_month(self):
        """Clear all data for the current month"""
        if messagebox.askyesno("Confirm", 
                              f"Are you sure you want to clear all data for {self.current_month.get()}?\nThis action cannot be undone."):
            self.data[self.current_month.get()] = {
                "income": 0,
                "expenses": [],
                "budget": 0
            }
            save_data(self.data)
            self.update_summary()
            messagebox.showinfo("Success", f"All data for {self.current_month.get()} has been cleared")


    def show_pie_chart(self):
        self.ensure_month_exists()

        month_data = self.data[self.current_month.get()]
        categories = {}
        for expense in month_data["expenses"]:
            categories.setdefault(expense["category"], 0)
            categories[expense["category"]] += expense["amount"]

        if not categories:
            messagebox.showinfo("No Data", "No expenses for this month.")
            return

        # Create modern-looking pie chart
        fig, ax = plt.subplots(figsize=(10, 7), facecolor=COLORS["bg_primary"])
        ax.set_facecolor(COLORS["bg_primary"])
        
        # Color palette for the pie chart
        colors = [
            COLORS["accent"],
            COLORS["success"],
            COLORS["warning"],
            COLORS["danger"],
            COLORS["accent_light"],
            "#8b5cf6",
            "#ec4899"
        ]
        
        wedges, texts, autotexts = ax.pie(
            categories.values(),
            labels=categories.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(categories)],
            textprops={'fontsize': 10, 'color': COLORS["text_primary"], 'weight': 'bold'}
        )
        
        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

        ax.set_title(
            f"Expenses Breakdown - {self.current_month.get()}",
            fontsize=14,
            color=COLORS["text_primary"],
            weight='bold',
            pad=20
        )

        plt.tight_layout()
        plt.show()


# --------------------------
# Run App
# --------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()