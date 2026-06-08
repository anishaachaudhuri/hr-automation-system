from passlib.context import CryptContext

from backend.audit import create_audit_log

from backend.db import (
    SessionLocal,
    engine
)

from backend.models import (
    Base,
    Admin,
    Requirement,
    Scientist
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

        create_audit_log(

            action_type="AUTH",

            description=
                "Failed login attempt"
        )

        return False

    valid = pwd_context.verify(
        password,
        admin.hashed_password
    )

    if valid:

        create_audit_log(

            action_type="AUTH",

            description=
                "Successful admin login"
        )

    else:

        create_audit_log(

            action_type="AUTH",

            description=
                "Failed login attempt"
        )

    return valid


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

            semantic_profile=
                "Looking for candidates with "
                "experience in machine learning, "
                "backend systems, APIs, research, "
                "scalable systems and intelligent "
                "applications.",

            minimum_gpa=8.0,

            required_skills=
                "python,machine learning",

            preferred_skills=
                "nlp,opencv",

            disallowed_branches=
                "biotechnology",

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

        "semantic_profile":
            req.semantic_profile,

        "minimum_gpa":
            req.minimum_gpa,

        "required_skills":
            req.required_skills,

        "preferred_skills":
            req.preferred_skills,

        "disallowed_branches":
            req.disallowed_branches,

        "skill_weight":
            req.skill_weight,

        "gpa_weight":
            req.gpa_weight,

        "research_weight":
            req.research_weight,

        "achievement_weight":
            req.achievement_weight,

        "updated_by":
            req.updated_by
    }


def update_requirements(data, username):

    db = SessionLocal()

    req = db.query(
        Requirement
    ).filter(
        Requirement.id == 1
    ).first()

    new_semantic_profile = data.get(
        "semantic_profile",
        data.get("semanticProfile", "")
    )

    new_minimum_gpa = data.get(
        "minimum_gpa",
        data.get("minimumGpa", 0)
    )

    new_required_skills = data.get(
        "required_skills",
        data.get("requiredSkills", "")
    )

    new_preferred_skills = data.get(
        "preferred_skills",
        data.get("preferredSkills", "")
    )

    new_disallowed_branches = data.get(
        "disallowed_branches",
        data.get("disallowedBranches", "")
    )

    new_skill_weight = data.get(
        "skill_weight",
        data.get("skillWeight", 0)
    )

    new_gpa_weight = data.get(
        "gpa_weight",
        data.get("gpaWeight", 0)
    )

    new_research_weight = data.get(
        "research_weight",
        data.get("researchWeight", 0)
    )

    new_achievement_weight = data.get(
        "achievement_weight",
        data.get("achievementWeight", 0)
    )

    if req.minimum_gpa != new_minimum_gpa:

        create_audit_log(

            action_type=
                "REQUIREMENT_CHANGE",

            changed_field=
                "minimum_gpa",

            old_value=
                req.minimum_gpa,

            new_value=
                new_minimum_gpa,

            description=
                f"Minimum GPA changed "
                f"from {req.minimum_gpa} "
                f"to {new_minimum_gpa}"
        )

    if req.required_skills != new_required_skills:

        create_audit_log(

            action_type=
                "REQUIREMENT_CHANGE",

            changed_field=
                "required_skills",

            old_value=
                req.required_skills,

            new_value=
                new_required_skills,

            description=
                "Required skills updated"
        )

    if req.preferred_skills != new_preferred_skills:

        create_audit_log(

            action_type=
                "REQUIREMENT_CHANGE",

            changed_field=
                "preferred_skills",

            old_value=
                req.preferred_skills,

            new_value=
                new_preferred_skills,

            description=
                "Preferred skills updated"
        )

    if req.disallowed_branches != new_disallowed_branches:

        create_audit_log(

            action_type=
                "REQUIREMENT_CHANGE",

            changed_field=
                "disallowed_branches",

            old_value=
                req.disallowed_branches,

            new_value=
                new_disallowed_branches,

            description=
                "Disallowed branches updated"
        )

    if req.skill_weight != new_skill_weight:

        create_audit_log(

            action_type=
                "REQUIREMENT_CHANGE",

            changed_field=
                "skill_weight",

            old_value=
                req.skill_weight,

            new_value=
                new_skill_weight,

            description=
                f"Skill weight changed "
                f"from {req.skill_weight} "
                f"to {new_skill_weight}"
        )

    if req.gpa_weight != new_gpa_weight:

        create_audit_log(

            action_type=
                "REQUIREMENT_CHANGE",

            changed_field=
                "gpa_weight",

            old_value=
                req.gpa_weight,

            new_value=
                new_gpa_weight,

            description=
                f"GPA weight changed "
                f"from {req.gpa_weight} "
                f"to {new_gpa_weight}"
        )

    if req.research_weight != new_research_weight:

        create_audit_log(

            action_type=
                "REQUIREMENT_CHANGE",

            changed_field=
                "research_weight",

            old_value=
                req.research_weight,

            new_value=
                new_research_weight,

            description=
                f"Research weight changed "
                f"from {req.research_weight} "
                f"to {new_research_weight}"
        )

    if req.achievement_weight != new_achievement_weight:

        create_audit_log(

            action_type=
                "REQUIREMENT_CHANGE",

            changed_field=
                "achievement_weight",

            old_value=
                req.achievement_weight,

            new_value=
                new_achievement_weight,

            description=
                f"Achievement weight changed "
                f"from {req.achievement_weight} "
                f"to {new_achievement_weight}"
        )

    # -------------------------
    # UPDATE VALUES
    # -------------------------

    req.semantic_profile = (
        new_semantic_profile
    )

    req.minimum_gpa = (
        new_minimum_gpa
    )

    req.required_skills = (
        new_required_skills
    )

    req.preferred_skills = (
        new_preferred_skills
    )

    req.disallowed_branches = (
        new_disallowed_branches
    )

    req.skill_weight = (
        new_skill_weight
    )

    req.gpa_weight = (
        new_gpa_weight
    )

    req.research_weight = (
        new_research_weight
    )

    req.achievement_weight = (
        new_achievement_weight
    )

    req.updated_by = username

    db.commit()

    db.close()

def create_default_scientists():

    db = SessionLocal()

    existing = db.query(Scientist).first()

    if existing:

        db.close()
        return

    scientists = [

        Scientist(
            name="Dr. R. Srinivasan",
            specialization="artificial intelligence",
            division="AI & Intelligent Systems",
            max_interns=10
        ),

        Scientist(
            name="Dr. Ananya Mehta",
            specialization="cybersecurity",
            division="Cyber Defence Systems",
            max_interns=10
        ),

        Scientist(
            name="Dr. Vivek Sharma",
            specialization="machine learning",
            division="Machine Learning Research",
            max_interns=10
        ),

        Scientist(
            name="Dr. Priya Nair",
            specialization="computer vision",
            division="Vision & Image Processing",
            max_interns=10
        ),

        Scientist(
            name="Dr. Arvind Rao",
            specialization="data science",
            division="Data Analytics Division",
            max_interns=10
        ),

        Scientist(
            name="Dr. Sneha Kulkarni",
            specialization="nlp",
            division="Language Computing Systems",
            max_interns=10
        ),

        Scientist(
            name="Dr. Karan Malhotra",
            specialization="cloud computing",
            division="Distributed Computing Systems",
            max_interns=10
        ),

        Scientist(
            name="Dr. Neeraj Bhatia",
            specialization="embedded systems",
            division="Embedded & Real-Time Systems",
            max_interns=10
        ),

        Scientist(
            name="Dr. Ishita Verma",
            specialization="web development",
            division="Software Applications Group",
            max_interns=10
        ),

        Scientist(
            name="Dr. Aditya Kapoor",
            specialization="network security",
            division="Secure Network Systems",
            max_interns=10
        )
    ]

    db.add_all(scientists)

    db.commit()

    db.close()