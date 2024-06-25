# ui.py
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import editor
import db
import json
import os
import competition_logic

class UI:
    def __init__(self, root):
        self.root = root
        self.editor = editor.Editor(root, self.open_editor)
        self.save_file_path = None
        self.manager_name = None
        self.club_id = None
        self.save_directory = None

    def create_widgets(self):
        self.clear_frame()
        self.title_label = tk.Label(self.root, text="Football Master", font=("Helvetica", 28, "bold"), fg="#ffffff", bg="#1f1f1f")
        self.title_label.pack(pady=20)

        button_frame = tk.Frame(self.root, bg="#1f1f1f")
        button_frame.pack(pady=20)

        new_game_button = tk.Button(button_frame, text="New Game", font=("Helvetica", 16), bg="#4CAF50", fg="#ffffff", command=self.new_game)
        new_game_button.grid(row=0, column=0, padx=20, pady=10)

        load_game_button = tk.Button(button_frame, text="Load Game", font=("Helvetica", 16), bg="#2196F3", fg="#ffffff", command=self.load_game)
        load_game_button.grid(row=1, column=0, padx=20, pady=10)

        editor_button = tk.Button(button_frame, text="Editor", font=("Helvetica", 16), bg="#FFC107", fg="#ffffff", command=self.open_editor)
        editor_button.grid(row=2, column=0, padx=20, pady=10)

        about_button = tk.Button(button_frame, text="About", font=("Helvetica", 16), bg="#FFC107", fg="#ffffff", command=self.show_about)
        about_button.grid(row=3, column=0, padx=20, pady=10)

        exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 16), bg="#f44336", fg="#ffffff", command=self.exit_game)
        exit_button.grid(row=4, column=0, padx=20, pady=10)

    def new_game(self):
        save_directory = filedialog.askdirectory(title="Select Folder to Save Game")
        if save_directory:
            self.create_manager_team_menu(save_directory)
        else:
            messagebox.showwarning("No Folder Selected", "You must select a folder to save the game.")

    def create_manager_team_menu(self, save_directory):
        self.clear_frame()
        self.title_label.config(text="Create New Game")

        self.manager_name_label = tk.Label(self.root, text="Manager Name:", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        self.manager_name_label.pack(pady=5)
        self.manager_name_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.manager_name_entry.pack(pady=5)

        self.continent_label = tk.Label(self.root, text="Select Continent:", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        self.continent_label.pack(pady=5)

        self.continent_combobox = ttk.Combobox(self.root, font=("Helvetica", 16), state="readonly")
        self.continent_combobox.pack(pady=5)
        self.continent_combobox.bind("<<ComboboxSelected>>", self.on_continent_selected)

        self.country_label = tk.Label(self.root, text="Select Country:", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        self.country_label.pack(pady=5)

        self.country_combobox = ttk.Combobox(self.root, font=("Helvetica", 16), state="readonly")
        self.country_combobox.pack(pady=5)
        self.country_combobox.bind("<<ComboboxSelected>>", self.on_country_selected)

        self.league_label = tk.Label(self.root, text="Select League:", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        self.league_label.pack(pady=5)

        self.league_combobox = ttk.Combobox(self.root, font=("Helvetica", 16), state="readonly")
        self.league_combobox.pack(pady=5)
        self.league_combobox.bind("<<ComboboxSelected>>", self.on_league_selected)

        self.team_label = tk.Label(self.root, text="Select Team:", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        self.team_label.pack(pady=5)

        self.team_listbox = tk.Listbox(self.root, font=("Helvetica", 16), height=10)
        self.team_listbox.pack(pady=5)

        self.start_game_button = tk.Button(self.root, text="Start Game", font=("Helvetica", 16), bg="#4CAF50", fg="#ffffff", command=lambda: self.start_game(save_directory))
        self.start_game_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Back", font=("Helvetica", 16), bg="#607D8B", fg="#ffffff", command=self.create_widgets)
        self.back_button.pack(pady=10)

        self.populate_continents()

    def populate_continents(self):
        continents = db.fetch_continents()
        self.continent_combobox['values'] = [continent[1] for continent in continents]

    def on_continent_selected(self, event):
        selected_continent = self.continent_combobox.get()
        continent_id = db.fetch_all("SELECT id FROM continents WHERE name=?", (selected_continent,))[0][0]
        countries = db.fetch_countries_by_continent(continent_id)
        self.country_combobox['values'] = [country[1] for country in countries]
        self.country_combobox.set('')
        self.league_combobox.set('')
        self.team_listbox.delete(0, tk.END)

    def on_country_selected(self, event):
        selected_country = self.country_combobox.get()
        country_id = db.fetch_all("SELECT id FROM countries WHERE name=?", (selected_country,))[0][0]
        leagues = db.fetch_leagues_by_country(country_id)
        self.league_combobox['values'] = [league[1] for league in leagues]
        self.league_combobox.set('')
        self.team_listbox.delete(0, tk.END)

    def on_league_selected(self, event):
        selected_league = self.league_combobox.get()
        league_id = db.fetch_all("SELECT id FROM leagues WHERE name=?", (selected_league,))[0][0]
        clubs = db.fetch_clubs_by_league(league_id)
        self.team_listbox.delete(0, tk.END)
        for club in clubs:
            self.team_listbox.insert(tk.END, f"{club[0]}: {club[1]}")

    def start_game(self, save_directory):
        manager_name = self.manager_name_entry.get()
        selected_team_index = self.team_listbox.curselection()
        if not selected_team_index:
            messagebox.showwarning("No Team Selected", "Please select a team.")
            return

        team_id = self.team_listbox.get(selected_team_index).split(":")[0]

        if manager_name and team_id:
            self.manager_name = manager_name
            self.club_id = team_id
            self.save_directory = save_directory
            self.save_file_path = os.path.join(save_directory, "save_game.json")
            self.save_game()
            self.show_main_menu()
        else:
            messagebox.showwarning("Incomplete Information", "Please enter manager name and select a team.")

    def show_main_menu(self):
        self.clear_frame()
        club_info = db.fetch_club_info(self.club_id)
        club_name = club_info[0][0]

        self.title_label.config(text=f"{self.manager_name}'s Management Dashboard")

        top_bar = tk.Frame(self.root, bg="#333")
        top_bar.pack(fill=tk.X)

        advance_button = tk.Button(top_bar, text="Advance to Next Match", font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", command=self.advance_to_next_match)
        advance_button.pack(side=tk.LEFT, padx=5, pady=5)

        fixtures_button = tk.Button(top_bar, text="Fixtures", font=("Helvetica", 12), bg="#2196F3", fg="#ffffff", command=self.view_fixtures)
        fixtures_button.pack(side=tk.LEFT, padx=5, pady=5)

        schedule_button = tk.Button(top_bar, text="Schedule", font=("Helvetica", 12), bg="#FFC107", fg="#ffffff", command=self.view_schedule)
        schedule_button.pack(side=tk.LEFT, padx=5, pady=5)

        options_button = tk.Button(top_bar, text="Options", font=("Helvetica", 12), bg="#607D8B", fg="#ffffff", command=self.options_menu)
        options_button.pack(side=tk.LEFT, padx=5, pady=5)

        save_button = tk.Button(top_bar, text="Save Game", font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", command=self.save_game)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

        competition_button = tk.Button(top_bar, text="Competition", font=("Helvetica", 12), bg="#4CAF50", fg="#ffffff", command=self.view_competition)
        competition_button.pack(side=tk.LEFT, padx=5, pady=5)

        info_frame = tk.Frame(self.root, bg="#1f1f1f")
        info_frame.pack(pady=20)

        club_label = tk.Label(info_frame, text=f"Club: {club_name}", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        club_label.grid(row=0, column=0, padx=10, pady=5)

        manager_label = tk.Label(info_frame, text=f"Manager: {self.manager_name}", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        manager_label.grid(row=1, column=0, padx=10, pady=5)

        save_label = tk.Label(info_frame, text=f"Save Directory: {self.save_directory}", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        save_label.grid(row=2, column=0, padx=10, pady=5)

        players_label = tk.Label(info_frame, text="Players:", font=("Helvetica", 16), fg="#ffffff", bg="#1f1f1f")
        players_label.grid(row=3, column=0, padx=10, pady=10)

        players_frame = tk.Frame(self.root, bg="#1f1f1f")
        players_frame.pack(pady=10)

        self.players_tree = ttk.Treeview(players_frame, columns=("Name", "Position", "Skill Level"), show="headings")
        self.players_tree.heading("Name", text="Name", command=lambda: self.sort_players("Name", False))
        self.players_tree.heading("Position", text="Position", command=lambda: self.sort_players("Position", False))
        self.players_tree.heading("Skill Level", text="Skill Level", command=lambda: self.sort_players("Skill Level", False))
        self.players_tree.pack(fill=tk.BOTH, expand=True)

        self.populate_players_tree()

    def populate_players_tree(self):
        for i in self.players_tree.get_children():
            self.players_tree.delete(i)

        players = db.fetch_players(self.club_id)
        for player in players:
            self.players_tree.insert("", tk.END, values=player)

    def sort_players(self, col, descending):
        data = [(self.players_tree.set(child, col), child) for child in self.players_tree.get_children('')]
        data.sort(reverse=descending)
        for i, (val, child) in enumerate(data):
            self.players_tree.move(child, '', i)
        self.players_tree.heading(col, command=lambda: self.sort_players(col, not descending))

    def advance_to_next_match(self):
        messagebox.showinfo("Advance to Next Match", "This functionality is not yet implemented.")

    def view_fixtures(self):
        messagebox.showinfo("View Fixtures", "This functionality is not yet implemented.")

    def view_schedule(self):
        messagebox.showinfo("View Schedule", "This functionality is not yet implemented.")

    def options_menu(self):
        messagebox.showinfo("Options Menu", "This functionality is not yet implemented.")

    def save_game(self):
        if self.manager_name and self.club_id and self.save_directory:
            save_data = {
                "manager_name": self.manager_name,
                "club_id": self.club_id,
                "save_directory": self.save_directory
            }
            with open(self.save_file_path, 'w') as save_file:
                json.dump(save_data, save_file)
            messagebox.showinfo("Game Saved", "Your game has been saved successfully!")
        else:
            messagebox.showerror("Error", "Cannot save the game. Missing required information.")

    def load_game(self):
        save_file_path = filedialog.askopenfilename(title="Select Save Game File", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if save_file_path:
            with open(save_file_path, 'r') as save_file:
                save_data = json.load(save_file)
                self.manager_name = save_data["manager_name"]
                self.club_id = save_data["club_id"]
                self.save_directory = save_data["save_directory"]
                self.save_file_path = save_file_path
                self.show_main_menu()
        else:
            messagebox.showwarning("No File Selected", "You must select a save file to load the game.")

    def view_competition(self):
        self.clear_frame()
        self.title_label.config(text="Competition Rankings")

        competition_id = 1  # Example competition ID
        rankings = competition_logic.get_rankings(competition_id)

        rankings_frame = tk.Frame(self.root, bg="#1f1f1f")
        rankings_frame.pack(pady=10)

        self.rankings_tree = ttk.Treeview(rankings_frame, columns=("Rank", "Club ID", "Points"), show="headings")
        self.rankings_tree.heading("Rank", text="Rank")
        self.rankings_tree.heading("Club ID", text="Club ID")
        self.rankings_tree.heading("Points", text="Points")
        self.rankings_tree.pack(fill=tk.BOTH, expand=True)

        for rank, (club_id, points) in enumerate(rankings, start=1):
            self.rankings_tree.insert("", tk.END, values=(rank, club_id, points))

        back_button = tk.Button(self.root, text="Back", font=("Helvetica", 16), bg="#607D8B", fg="#ffffff", command=self.show_main_menu)
        back_button.pack(pady=10)

    def manage_team(self):
        messagebox.showinfo("Manage Team", "This functionality is not yet implemented.")

    def show_about(self):
        about_text = (
            "Football Master\n\n"
            "Version 1.0\n"
            "Developed by [Your Name]\n\n"
            "Football Master is a soccer management game where you can "
            "manage your own team, make strategic decisions, and lead your "
            "team to victory!"
        )
        messagebox.showinfo("About Football Master", about_text)

    def exit_game(self):
        self.root.quit()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def open_editor(self):
        self.editor.clear_frame()
        self.editor.edit_continents()
        # Implement other editor functions as needed
