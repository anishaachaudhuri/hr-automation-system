import sqlite3
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_NAME = os.path.join(
    BASE_DIR,
    "../data/hr_system.db"
)


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

        name TEXT,

        filename TEXT,

        skills TEXT,

        tenth REAL,

        twelfth REAL,

        gpa REAL,

        selected BOOLEAN,

        score REAL,

        semantic_score REAL,

        top_semantic_chunk TEXT,

        reasons TEXT
    )
    """)

    conn.commit()

    conn.close()


def save_candidate(data):

    conn = get_connection()

    cursor = conn.cursor()

    semantic_result = data.get(
        "semantic_matching",
        {}
    )

    semantic_score = semantic_result.get(
        "average_similarity",
        0
    )

    top_chunks = semantic_result.get(
        "top_chunks",
        []
    )

    top_chunk = ""

    if top_chunks:

        top_chunk = top_chunks[0].get(
            "text",
            ""
        )

    print("Saving candidate...")
    print(data)

    cursor.execute("""
    INSERT INTO candidates (

        name,

        filename,

        skills,

        tenth,

        twelfth,

        gpa,

        selected,

        score,

        semantic_score,

        top_semantic_chunk,

        reasons

    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        data.get(
            "name",
            "Unknown"
        ),

        data.get(
            "filename",
            ""
        ),

        ", ".join(
            data.get(
                "skills",
                []
            )
        ),

        data.get(
            "marks",
            {}
        ).get(
            "tenth"
        ),

        data.get(
            "marks",
            {}
        ).get(
            "twelfth"
        ),

        data.get(
            "marks",
            {}
        ).get(
            "gpa"
        ),

        data.get(
            "evaluation",
            {}
        ).get(
            "selected",
            False
        ),

        data.get(
            "evaluation",
            {}
        ).get(
            "score",
            0
        ),

        semantic_score,

        top_chunk,

        ", ".join(
            data.get(
                "evaluation",
                {}
            ).get(
                "reasons",
                []
            )
        )
    ))

    conn.commit()

    print(
        "Candidate inserted successfully"
    )

    conn.close()