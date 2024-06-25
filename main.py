# main.py
import tkinter as tk
import db
import ui

def main():
    root = tk.Tk()
    app = ui.UI(root)
    db.create_database()  # Ensure the database is created
    app.create_widgets()
    root.mainloop()

if __name__ == "__main__":
    main()
