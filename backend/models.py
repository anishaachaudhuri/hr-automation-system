from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime
)
from sqlalchemy.sql import func
from backend.db import Base

class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    filename = Column(String)

    skills = Column(Text)

    tenth = Column(Float)

    twelfth = Column(Float)

    gpa = Column(Float)

    selected = Column(Boolean)

    score = Column(Float)

    semantic_score = Column(Float)

    embedding = Column(Vector(384))

    top_semantic_chunk = Column(Text)

    reasons = Column(Text)


class Admin(Base):

    __tablename__ = "admins"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True
    )

    hashed_password = Column(String)


class Requirement(Base):

    __tablename__ = "requirements"

    id = Column(
        Integer,
        primary_key=True
    )

    semantic_profile = Column(Text)

    minimum_gpa = Column(Float)

    required_skills = Column(Text)

    preferred_skills = Column(Text)

    disallowed_branches = Column(Text)

    skill_weight = Column(Float)

    gpa_weight = Column(Float)

    research_weight = Column(Float)

    achievement_weight = Column(Float)

    updated_by = Column(String)

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )

    action_type = Column(String)

    changed_field = Column(String)

    old_value = Column(Text)

    new_value = Column(Text)

    description = Column(Text)

    timestamp = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )