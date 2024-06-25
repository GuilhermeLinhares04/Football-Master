# db.py
import sqlite3

def create_database():
    connection = sqlite3.connect("football_master.db")
    cursor = connection.cursor()

    # Create continents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS continents (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    # Create countries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            continent_id INTEGER,
            FOREIGN KEY (continent_id) REFERENCES continents(id)
        )
    """)

    # Create leagues table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leagues (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(id)
        )
    """)

    # Create clubs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clubs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country_id INTEGER,
            league_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(id),
            FOREIGN KEY (league_id) REFERENCES leagues(id)
        )
    """)

    # Create players table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country_id INTEGER,
            club_id INTEGER,
            position TEXT NOT NULL,
            skill_level INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(id),
            FOREIGN KEY (club_id) REFERENCES clubs(id)
        )
    """)

    # Create managers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country_id INTEGER,
            club_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(id),
            FOREIGN KEY (club_id) REFERENCES clubs(id)
        )
    """)

    # Create competitions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            league_id INTEGER,
            FOREIGN KEY (league_id) REFERENCES leagues(id)
        )
    """)

    # Create matches table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            competition_id INTEGER,
            home_club_id INTEGER,
            away_club_id INTEGER,
            home_score INTEGER,
            away_score INTEGER,
            match_date TEXT,
            FOREIGN KEY (competition_id) REFERENCES competitions(id),
            FOREIGN KEY (home_club_id) REFERENCES clubs(id),
            FOREIGN KEY (away_club_id) REFERENCES clubs(id)
        )
    """)

    connection.commit()
    connection.close()

def execute_query(query, params=()):
    connection = sqlite3.connect("football_master.db")
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()

def fetch_all(query, params=()):
    connection = sqlite3.connect("football_master.db")
    cursor = connection.cursor()
    cursor.execute(query, params)
    records = cursor.fetchall()
    connection.close()
    return records

def fetch_clubs():
    return fetch_all("SELECT id, name FROM clubs")

def fetch_clubs_by_league(league_id):
    return fetch_all("SELECT id, name FROM clubs WHERE league_id=?", (league_id,))

def fetch_club_info(club_id):
    return fetch_all("SELECT name, country_id FROM clubs WHERE id=?", (club_id,))

def fetch_manager_info(manager_name, club_id):
    return fetch_all("SELECT id, name FROM managers WHERE name=? AND club_id=?", (manager_name, club_id))

def fetch_players(club_id):
    return fetch_all("SELECT name, position, skill_level FROM players WHERE club_id=?", (club_id,))

def fetch_continents():
    return fetch_all("SELECT id, name FROM continents")

def fetch_countries_by_continent(continent_id):
    return fetch_all("SELECT id, name FROM countries WHERE continent_id=?", (continent_id,))

def fetch_leagues_by_country(country_id):
    return fetch_all("SELECT id, name FROM leagues WHERE country_id=?", (country_id,))

def fetch_competitions_by_league(league_id):
    return fetch_all("SELECT id, name FROM competitions WHERE league_id=?", (league_id,))

def fetch_matches_by_competition(competition_id):
    return fetch_all("SELECT id, home_club_id, away_club_id, home_score, away_score, match_date FROM matches WHERE competition_id=?", (competition_id,))
