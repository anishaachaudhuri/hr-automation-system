import sqlite3

DB_NAME = "data/hr_system.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        skills TEXT,
        tenth REAL,
        twelfth REAL,
        gpa REAL,
        selected BOOLEAN,
        score REAL,
        reasons TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_candidate(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates (
        filename,
        skills,
        tenth,
        twelfth,
        gpa,
        selected,
        score,
        reasons
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["filename"],
        ", ".join(data["skills"]),
        data["marks"]["tenth"],
        data["marks"]["twelfth"],
        data["marks"]["gpa"],
        data["evaluation"]["selected"],
        data["evaluation"].get("score", 0),
        ", ".join(data["evaluation"].get("reasons", []))
    ))

    conn.commit()
    conn.close()