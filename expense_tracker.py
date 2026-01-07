import sqlite3
import datetime

# Connect to SQLite database
conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# Create expenses table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, amount REAL, description TEXT, date TEXT)''')
conn.commit()

def add_expense(amount, description, date):
    """Add a new expense to the database."""
    c.execute("INSERT INTO expenses (amount, description, date) VALUES (?, ?, ?)", (amount, description, date))
    conn.commit()

def view_expenses():
    """View all expenses stored in the database."""
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    if expenses:
        for expense in expenses:
            print(expense)
    else:
        print("No expenses found.")

def query_expenses(querychoice):
    try:
        id_expense = int(querychoice)
    except (ValueError, TypeError):
        return None
    c.execute("SELECT * FROM expenses WHERE id = ?", (id_expense,))
    return c.fetchone()

def update_expenses(id_, new_amount=None, new_desc=None, new_date=None):
    fields = []
    params = []
    if new_amount is not None:
        fields.append("amount = ?")
        params.append(new_amount)
    if new_desc is not None:
        fields.append("description = ?")
        params.append(new_desc)
    if new_date is not None:
        fields.append("date = ?")
        params.append(new_date)
    if not fields:
        return False
    params.append(id_)
    sql = "UPDATE expenses SET " + ", ".join(fields) + " WHERE id = ?"
    c.execute(sql, tuple(params))
    conn.commit()
    return c.rowcount > 0

def delete_expenses(id_):
    c.execute("DELETE FROM expenses WHERE id = ?", (id_,))
    conn.commit()

def sum_expenses():
    c.execute("SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses GROUP BY month ORDER BY month")
    sumarry = c.fetchall()
    if sumarry:
        for month, total in sumarry:
            print(f"{month}: {total:.2f}")

def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expenses")
        print("4. Delete Expenses")
        print("5. Expenses Summary")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            add_expense(amount, description, date)
            print("Expense added successfully.")

        elif choice == '2':
            print("\nAll Expenses:")
            view_expenses()
            input("Press Any To Continue")

        elif choice == '3':
            print("\nSelect Expenses That You Want To Modify")
            view_expenses()
            
            # find id
            while True:
                querychoice = input("Enter id: ").strip()
                row = query_expenses(querychoice)
                if row:
                    print("Found:", row)
                    id_to_edit = row[0]
                    break
                print("id not found please try again")

            #input new amount 
            try:
                newamountinput = input("New amount (leave blank to keep current): ").strip()
                newamount = float(newamountinput) if newamountinput else None
            except ValueError:
                print("Invalid amount entered. Update cancelled.")
                continue
            #input new description
            newdescription = input("New description (leave blank to keep current): ").strip() or None
            dateinput = input("New date YYYY-MM-DD (leave blank to set to today's date): ").strip()
            if dateinput:
                newdate = dateinput
            else:
                newdate = datetime.datetime.now().strftime("%Y-%m-%d")

            success = update_expenses(id_to_edit, newamount, newdescription, newdate)
            if success:
                print("Expense updated successfully.")
                input("Press Any Key To Continue")
            else:
                print("No changes made or update failed.")
            
        elif choice == '4':
            print("\nSelect Expenses That You Want To Delete")
            view_expenses()

            while True:
                querychoice = input("Enter id: ").strip()
                row = query_expenses(querychoice)
                if row:
                    print("Found:", row)
                    id_to_delete = row[0]
                    break
                print("id not found please try again")

            confirmdeletechoice = input("Are You Sure?")

            if confirmdeletechoice == "yes":
                delete_expenses(id_to_delete)
                print("The Expense Has Been Deleted Sucessfully")
                input("Press Any Key To Continue")
            elif confirmdeletechoice == "no":
                print("Delete Is Cancelled")
                input("Press Any To Continue")

        elif choice == '5':
            print("\nExpenses Summary:")
            sum_expenses()
            input("Press Any Key To Continue")

        elif choice == '6':
            print("Goodbye")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
