# editor.py
import tkinter as tk
from tkinter import simpledialog, messagebox
import db

class Editor:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def display_data(self, table_name):
        records = db.fetch_all(f"SELECT * FROM {table_name}")
        data_frame = tk.Frame(self.root, bg="#1f1f1f")
        data_frame.pack(pady=10)

        for index, record in enumerate(records):
            record_label = tk.Label(data_frame, text=record, font=("Helvetica", 12), fg="#ffffff", bg="#1f1f1f")
            record_label.grid(row=index, column=0, padx=5, pady=5)

    def edit_continents(self):
        self.clear_frame()
        self.display_data("continents")

        add_button = tk.Button(self.root, text="Add Continent", font=("Helvetica", 16), bg="#4CAF50", fg="#ffffff", command=self.add_continent)
        add_button.pack(pady=5)

        delete_button = tk.Button(self.root, text="Delete Continent", font=("Helvetica", 16), bg="#f44336", fg="#ffffff", command=self.delete_continent)
        delete_button.pack(pady=5)

        back_button = tk.Button(self.root, text="Back", font=("Helvetica", 16), bg="#607D8B", fg="#ffffff", command=self.back_callback)
        back_button.pack(pady=10)

    def add_continent(self):
        name = simpledialog.askstring("Input", "Enter Continent Name:")
        if name:
            db.execute_query("INSERT INTO continents (name) VALUES (?)", (name,))
            messagebox.showinfo("Success", "Continent added successfully!")
            self.edit_continents()

    def delete_continent(self):
        id = simpledialog.askinteger("Input", "Enter Continent ID to Delete:")
        if id:
            db.execute_query("DELETE FROM continents WHERE id=?", (id,))
            messagebox.showinfo("Success", "Continent deleted successfully!")
            self.edit_continents()

    # Implement similar methods for countries, clubs, players, and managers...
