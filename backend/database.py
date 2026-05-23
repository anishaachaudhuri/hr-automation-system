from sqlalchemy.orm import Session

from backend.db import (
    SessionLocal,
    engine
)

from backend.models import (
    Base,
    Candidate
)

from backend.services.nlp_engine import (
    embedding_model
)

Base.metadata.create_all(
    bind=engine
)


def get_connection():

    return SessionLocal()


def create_table():

    Base.metadata.create_all(
        bind=engine
    )


def save_candidate(data):

    db: Session = SessionLocal()

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

    embedding_text = " ".join(
        data.get("skills", [])
    )

    embedding_vector = embedding_model.encode(
        embedding_text
    ).tolist()

    candidate = Candidate(

        name=data.get(
            "name",
            "Unknown"
        ),

        filename=data.get(
            "filename",
            ""
        ),

        skills=", ".join(
            data.get(
                "skills",
                []
            )
        ),

        tenth=data.get(
            "marks",
            {}
        ).get("tenth"),

        twelfth=data.get(
            "marks",
            {}
        ).get("twelfth"),

        gpa=data.get(
            "marks",
            {}
        ).get("gpa"),

        selected=data.get(
            "evaluation",
            {}
        ).get(
            "selected",
            False
        ),

        score=data.get(
            "evaluation",
            {}
        ).get(
            "score",
            0
        ),

        semantic_score=semantic_score,
        embedding=embedding_vector,
        top_semantic_chunk=top_chunk,

        reasons=", ".join(
            data.get(
                "evaluation",
                {}
            ).get(
                "reasons",
                []
            )
        )
    )

    db.add(candidate)

    db.commit()

    db.close()