import sqlite3
from pathlib import Path

# Database location
DB_PATH = Path("data/database/jobs.db")

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_database():

    conn = create_connection()
    cursor = conn.cursor()

    with open("sql/create_tables.sql", "r") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()

    print("Database initialized.")

if __name__ == "__main__":
    initialize_database()