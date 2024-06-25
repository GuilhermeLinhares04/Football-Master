# delete_data.py
import sqlite3

def connect_to_db():
    return sqlite3.connect("football_master.db")

def delete_all_data():
    connection = connect_to_db()
    cursor = connection.cursor()

    # Delete all data from tables
    cursor.execute("DELETE FROM managers")
    cursor.execute("DELETE FROM players")
    cursor.execute("DELETE FROM clubs")
    cursor.execute("DELETE FROM leagues")
    cursor.execute("DELETE FROM countries")
    cursor.execute("DELETE FROM continents")

    connection.commit()
    connection.close()

if __name__ == "__main__":
    delete_all_data()
    print("All data has been deleted from the database.")
