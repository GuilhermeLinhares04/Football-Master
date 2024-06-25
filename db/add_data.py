# add_data.py
import sqlite3

def connect_to_db():
    return sqlite3.connect("football_master.db")

def add_continent(id, name):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO continents (id, name) VALUES (?, ?)", (id, name))
    connection.commit()
    connection.close()

def add_country(id, name, continent_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO countries (id, name, continent_id) VALUES (?, ?, ?)", (id, name, continent_id))
    connection.commit()
    connection.close()

def add_league(id, name, country_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO leagues (id, name, country_id) VALUES (?, ?, ?)", (id, name, country_id))
    connection.commit()
    connection.close()

def add_club(id, name, country_id, league_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO clubs (id, name, country_id, league_id) VALUES (?, ?, ?, ?)", (id, name, country_id, league_id))
    connection.commit()
    connection.close()

def add_player(id, name, country_id, club_id, position, skill_level):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO players (id, name, country_id, club_id, position, skill_level) VALUES (?, ?, ?, ?, ?, ?)", 
                   (id, name, country_id, club_id, position, skill_level))
    connection.commit()
    connection.close()

def add_manager(id, name, country_id, club_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO managers (id, name, country_id, club_id) VALUES (?, ?, ?, ?)", (id, name, country_id, club_id))
    connection.commit()
    connection.close()

def add_competition(id, name, league_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO competitions (id, name, league_id) VALUES (?, ?, ?)", (id, name, league_id))
    connection.commit()
    connection.close()

def add_match(id, competition_id, home_club_id, away_club_id, home_score, away_score, match_date):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO matches (id, competition_id, home_club_id, away_club_id, home_score, away_score, match_date) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (id, competition_id, home_club_id, away_club_id, home_score, away_score, match_date))
    connection.commit()
    connection.close()

if __name__ == "__main__":
    # Example data
    add_continent(1, "Europe")
    add_continent(2, "South America")

    add_country(1, "England", 1)
    add_country(2, "Brazil", 2)

    add_league(1, "Premier League", 1)
    add_league(2, "Serie A", 2)

    add_club(1, "Manchester United", 1, 1)
    add_club(2, "Chelsea", 1, 1)
    add_club(3, "Flamengo", 2, 2)
    add_club(4, "Palmeiras", 2, 2)

    add_player(1, "Player One", 1, 1, "Forward", 85)
    add_player(2, "Player Two", 1, 2, "Midfielder", 80)
    add_player(3, "Player Three", 2, 3, "Defender", 78)
    add_player(4, "Player Four", 2, 4, "Goalkeeper", 82)

    add_manager(1, "Manager One", 1, 1)
    add_manager(2, "Manager Two", 2, 2)

    add_competition(1, "Premier League 2024", 1)
    add_competition(2, "Serie A 2024", 2)

    add_match(1, 1, 1, 2, 3, 2, "2024-09-01")
    add_match(2, 1, 2, 1, 1, 1, "2024-09-08")
    add_match(3, 2, 3, 4, 2, 1, "2024-09-01")
    add_match(4, 2, 4, 3, 0, 0, "2024-09-08")
