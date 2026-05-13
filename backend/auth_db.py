import sqlite3
from passlib.context import CryptContext

DB_NAME = "data/hr_system.db"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_auth_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        hashed_password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requirements (
        id INTEGER PRIMARY KEY,
        minimum_gpa REAL,
        required_skills TEXT,
        preferred_skills TEXT,
        disallowed_branches TEXT,
        skill_weight REAL,
        gpa_weight REAL,
        research_weight REAL,
        achievement_weight REAL,
        updated_by TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_default_admin():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM admins WHERE username=?",
        ("admin",)
    )

    admin = cursor.fetchone()

    if not admin:

        hashed_password = pwd_context.hash(
            "admin123"
        )

        cursor.execute(
            "INSERT INTO admins (username, hashed_password) VALUES (?, ?)",
            ("admin", hashed_password)
        )

    conn.commit()
    conn.close()


def verify_admin(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM admins WHERE username=?",
        (username,)
    )

    admin = cursor.fetchone()

    conn.close()

    if not admin:
        return False

    return pwd_context.verify(
        password,
        admin["hashed_password"]
    )


def create_default_requirements():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM requirements WHERE id=1"
    )

    existing = cursor.fetchone()

    if not existing:

        cursor.execute("""
        INSERT INTO requirements (
            id,
            minimum_gpa,
            required_skills,
            preferred_skills,
            disallowed_branches,
            skill_weight,
            gpa_weight,
            research_weight,
            achievement_weight,
            updated_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1,
            8.0,
            "python,machine learning",
            "nlp,opencv",
            "biotechnology",
            40,
            25,
            20,
            15,
            "system"
        ))

    conn.commit()
    conn.close()


def get_requirements():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM requirements WHERE id=1"
    )

    data = cursor.fetchone()

    conn.close()

    return dict(data)


def update_requirements(data, username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE requirements
    SET
        minimum_gpa=?,
        required_skills=?,
        preferred_skills=?,
        disallowed_branches=?,
        skill_weight=?,
        gpa_weight=?,
        research_weight=?,
        achievement_weight=?,
        updated_by=?
    WHERE id=1
    """, (
        data["minimum_gpa"],
        data["required_skills"],
        data["preferred_skills"],
        data["disallowed_branches"],
        data["skill_weight"],
        data["gpa_weight"],
        data["research_weight"],
        data["achievement_weight"],
        username
    ))

    conn.commit()
    conn.close()