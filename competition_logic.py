# competition_logic.py
import sqlite3

def connect_to_db():
    return sqlite3.connect("football_master.db")

def calculate_points(matches):
    points = {}
    for match in matches:
        home_club_id = match[1]
        away_club_id = match[2]
        home_score = match[3]
        away_score = match[4]

        if home_club_id not in points:
            points[home_club_id] = 0
        if away_club_id not in points:
            points[away_club_id] = 0

        if home_score > away_score:
            points[home_club_id] += 3
        elif away_score > home_score:
            points[away_club_id] += 3
        else:
            points[home_club_id] += 1
            points[away_club_id] += 1

    return points

def get_rankings(competition_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id, home_club_id, away_club_id, home_score, away_score FROM matches WHERE competition_id=?", (competition_id,))
    matches = cursor.fetchall()
    connection.close()

    points = calculate_points(matches)
    rankings = sorted(points.items(), key=lambda item: item[1], reverse=True)

    return rankings

if __name__ == "__main__":
    competition_id = 1
    rankings = get_rankings(competition_id)
    for rank, (club_id, points) in enumerate(rankings, start=1):
        print(f"Rank {rank}: Club ID {club_id} - {points} points")
