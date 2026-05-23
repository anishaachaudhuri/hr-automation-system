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
    "id": req.id,
    "semantic_profile": req.semantic_profile,
    "minimum_gpa": req.minimum_gpa,
    "required_skills": req.required_skills,
    "preferred_skills": req.preferred_skills,
    "disallowed_branches": req.disallowed_branches,
    "skill_weight": req.skill_weight,
    "gpa_weight": req.gpa_weight,
    "research_weight": req.research_weight,
    "achievement_weight": req.achievement_weight,
    "updated_by": req.updated_by
}


def update_requirements(data, username):

    db = SessionLocal()

    req = db.query(
        Requirement
    ).filter(
        Requirement.id == 1
    ).first()

    req.semantic_profile = data.get(
        "semantic_profile",
        data.get("semanticProfile", "")
    )

    req.minimum_gpa = data.get(
        "minimum_gpa",
        data.get("minimumGpa", 0)
    )

    req.required_skills = data.get(
        "required_skills",
        data.get("requiredSkills", "")
    )

    req.preferred_skills = data.get(
        "preferred_skills",
        data.get("preferredSkills", "")
    )

    req.disallowed_branches = data.get(
        "disallowed_branches",
        data.get("disallowedBranches", "")
    )

    req.skill_weight = data.get(
        "skill_weight",
        data.get("skillWeight", 0)
    )

    req.gpa_weight = data.get(
        "gpa_weight",
        data.get("gpaWeight", 0)
    )

    req.research_weight = data.get(
        "research_weight",
        data.get("researchWeight", 0)
    )

    req.achievement_weight = data.get(
        "achievement_weight",
        data.get("achievementWeight", 0)
    )

    req.updated_by = username

    db.commit()

    db.close()