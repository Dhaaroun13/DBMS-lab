import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

DB_FILE = "bank.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS account (
    accno   INTEGER PRIMARY KEY,
    cname   TEXT    NOT NULL,
    balance REAL    NOT NULL DEFAULT 0 CHECK (balance >= 0)
);
"""


class BankError(Exception):
    """Raised for any user-facing problem (bad input, no funds, ...)."""

class BankDB:
    def __init__(self, path=DB_FILE):
        self.conn = sqlite3.connect(path)
        self.conn.execute(SCHEMA)
        self.conn.commit()

    def all_accounts(self):
        return self.conn.execute(
            "SELECT accno, cname, balance FROM account ORDER BY accno"
        ).fetchall()

    def get(self, accno):
        row = self.conn.execute(
            "SELECT accno, cname, balance FROM account WHERE accno = ?", (accno,)
        ).fetchone()
        if row is None:
            raise BankError(f"Account {accno} does not exist.")
        return row

    # `with self.conn:` = COMMIT if the block succeeds, ROLLBACK if it fails
    def add(self, accno, cname, balance):
        if not cname.strip():
            raise BankError("Customer name cannot be empty.")
        if balance < 0:
            raise BankError("Opening balance cannot be negative.")
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO account (accno, cname, balance) VALUES (?, ?, ?)",
                    (accno, cname.strip(), balance),
                )
        except sqlite3.IntegrityError:
            raise BankError(f"Account {accno} already exists.")

    def rename(self, accno, cname):
        self.get(accno)
        if not cname.strip():
            raise BankError("Customer name cannot be empty.")
        with self.conn:
            self.conn.execute(
                "UPDATE account SET cname = ? WHERE accno = ?", (cname.strip(), accno)
            )

    def delete(self, accno):
        self.get(accno)
        with self.conn:
            self.conn.execute("DELETE FROM account WHERE accno = ?", (accno,))

    def deposit(self, accno, amount):
        if amount <= 0:
            raise BankError("Deposit amount must be greater than zero.")
        self.get(accno)
        with self.conn:
            self.conn.execute(
                "UPDATE account SET balance = balance + ? WHERE accno = ?",
                (amount, accno),
            )
        return self.get(accno)[2]

    def withdraw(self, accno, amount):
        if amount <= 0:
            raise BankError("Withdrawal amount must be greater than zero.")
        self.get(accno)
        with self.conn:
            cur = self.conn.execute(
                "UPDATE account SET balance = balance - ? "
                "WHERE accno = ? AND balance >= ?",
                (amount, accno, amount),
            )
        if cur.rowcount == 0:
            raise BankError("Insufficient balance.")
        return self.get(accno)[2]


def parse_accno(text):
    try:
        return int(text.strip())
    except ValueError:
        raise BankError("Account number must be a whole number.")


def parse_money(text, blank_ok=False):
    text = text.strip()
    if not text and blank_ok:
        return 0.0
    try:
        return float(text)
    except ValueError:
        raise BankError("Balance must be a number.")


class BankApp(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.title("Banking System")
        self.resizable(False, False)
        self.accno = tk.StringVar()
        self.cname = tk.StringVar()
        self.balance = tk.StringVar()
        self._build()
        self.refresh()

    def _build(self):
        form = ttk.LabelFrame(self, text="Account details", padding=10)
        form.grid(row=0, column=0, padx=10, pady=(10, 4), sticky="ew")
        fields = [
            ("Account No", self.accno),
            ("Customer Name", self.cname),
            ("Balance (Rs)", self.balance),
        ]
        for r, (label, var) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=r, column=0, sticky="w", pady=3)
            ttk.Entry(form, textvariable=var, width=30).grid(row=r, column=1, padx=8)

        buttons = ttk.Frame(self)
        buttons.grid(row=1, column=0, padx=10, pady=4)
        actions = [
            ("Insert", self.insert),
            ("Update", self.update),
            ("Delete", self.delete),
            ("Clear", self.clear),
            ("Deposit", self.deposit),
            ("Withdraw", self.withdraw),
            ("Exit", self.destroy),
        ]
        for i, (text, cmd) in enumerate(actions):
            ttk.Button(buttons, text=text, command=cmd, width=10).grid(
                row=i // 4, column=i % 4, padx=3, pady=3
            )

        cols = ("accno", "cname", "balance")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for col, title, width in [
            ("accno", "Account No", 100),
            ("cname", "Customer Name", 190),
            ("balance", "Balance (Rs)", 110),
        ]:
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="w")
        self.tree.grid(row=2, column=0, padx=10, pady=(4, 10))
        self.tree.bind("<<TreeviewSelect>>", self.on_select)


    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for accno, cname, balance in self.db.all_accounts():
            self.tree.insert("", "end", values=(accno, cname, f"{balance:.2f}"))

    def on_select(self, _event=None):
        sel = self.tree.selection()
        if sel:
            accno, cname, balance = self.tree.item(sel[0], "values")
            self.accno.set(accno)
            self.cname.set(cname)
            self.balance.set(balance)

    def error(self, err):
        messagebox.showerror("Banking System", str(err), parent=self)

    def info(self, msg):
        messagebox.showinfo("Banking System", msg, parent=self)

    def ask_amount(self, title, prompt):
        return simpledialog.askfloat(title, prompt, parent=self, minvalue=0.01)

    def insert(self):
        try:
            accno = parse_accno(self.accno.get())
            balance = parse_money(self.balance.get(), blank_ok=True)
            self.db.add(accno, self.cname.get(), balance)
        except BankError as e:
            return self.error(e)
        self.refresh()
        self.info("Record inserted successfully.")

    def update(self):
        try:
            accno = parse_accno(self.accno.get())
            self.db.rename(accno, self.cname.get())
        except BankError as e:
            return self.error(e)
        self.refresh()
        self.info("Record updated successfully. "
                  "(Balance changes only through Deposit / Withdraw.)")

    def delete(self):
        try:
            accno = parse_accno(self.accno.get())
            self.db.get(accno)
            if not messagebox.askyesno("Banking System",
                                       f"Delete account {accno}?", parent=self):
                return
            self.db.delete(accno)
        except BankError as e:
            return self.error(e)
        self.clear()
        self.refresh()
        self.info("Record deleted.")

    def clear(self):
        for var in (self.accno, self.cname, self.balance):
            var.set("")
        self.tree.selection_remove(self.tree.selection())

    def deposit(self):
        self._transact("Deposit", "Enter the amount to be deposited (Rs):",
                       self.db.deposit)

    def withdraw(self):
        self._transact("Withdraw", "Enter the amount to be withdrawn (Rs):",
                       self.db.withdraw)

    def _transact(self, title, prompt, operation):
        try:
            accno = parse_accno(self.accno.get())
            self.db.get(accno)
            amount = self.ask_amount(title, prompt)
            if amount is None:          # dialog cancelled
                return
            new_balance = operation(accno, amount)
        except BankError as e:
            return self.error(e)
        self.refresh()
        self.balance.set(f"{new_balance:.2f}")
        self.info(f"Current balance is Rs {new_balance:.2f}")


if __name__ == "__main__":
    BankApp(BankDB()).mainloop()
