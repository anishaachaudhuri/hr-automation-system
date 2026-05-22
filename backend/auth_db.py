from passlib.context import CryptContext

from backend.db import (
    SessionLocal,
    engine
)

from backend.models import (
    Base,
    Admin,
    Requirement
)

Base.metadata.create_all(
    bind=engine
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def create_auth_tables():

    Base.metadata.create_all(
        bind=engine
    )


def create_default_admin():

    db = SessionLocal()

    admin = db.query(Admin).filter(
        Admin.username == "admin"
    ).first()

    if not admin:

        hashed_password = pwd_context.hash(
            "drdo123"
        )

        admin = Admin(
            username="admin",
            hashed_password=hashed_password
        )

        db.add(admin)

        db.commit()

    db.close()


def verify_admin(username, password):

    db = SessionLocal()

    admin = db.query(Admin).filter(
        Admin.username == username
    ).first()

    db.close()

    if not admin:
        return False

    return pwd_context.verify(
        password,
        admin.hashed_password
    )


def create_default_requirements():

    db = SessionLocal()

    existing = db.query(
        Requirement
    ).filter(
        Requirement.id == 1
    ).first()

    if not existing:

        req = Requirement(

            id=1,

            semantic_profile="Looking for candidates with experience in machine learning, backend systems, APIs, research, scalable systems and intelligent applications.",

            minimum_gpa=8.0,

            required_skills="python,machine learning",

            preferred_skills="nlp,opencv",

            disallowed_branches="biotechnology",

            skill_weight=40,

            gpa_weight=25,

            research_weight=20,

            achievement_weight=15,

            updated_by="system"
        )

        db.add(req)

        db.commit()

    db.close()


def get_requirements():

    db = SessionLocal()

    req = db.query(
        Requirement
    ).filter(
        Requirement.id == 1
    ).first()

    db.close()

    return {
        key: value
        for key, value
        in req.__dict__.items()
        if key != "_sa_instance_state"
    }


def update_requirements(data, username):

    db = SessionLocal()

    req = db.query(
        Requirement
    ).filter(
        Requirement.id == 1
    ).first()

    req.semantic_profile = data["semantic_profile"]

    req.minimum_gpa = data["minimum_gpa"]

    req.required_skills = data["required_skills"]

    req.preferred_skills = data["preferred_skills"]

    req.disallowed_branches = data["disallowed_branches"]

    req.skill_weight = data["skill_weight"]

    req.gpa_weight = data["gpa_weight"]

    req.research_weight = data["research_weight"]

    req.achievement_weight = data["achievement_weight"]

    req.updated_by = username

    db.commit()

    db.close()