from unittest import result
from backend.models import Candidate
from backend.serializers import (
    candidate_to_dict
)
from sqlalchemy import text

from backend.services.nlp_engine import (
    embedding_model
)
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Form,
    Request,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse

from starlette.middleware.sessions import SessionMiddleware

import shutil
import os
import fitz

from backend.auth_db import (
    create_auth_tables,
    create_default_admin,
    create_default_requirements,
    verify_admin,
    get_requirements,
    update_requirements
)

from backend.database import (
    create_table,
    save_candidate,
    get_connection
)

from backend.services.parser import (
    extract_skills,
    extract_marks,
    evaluate_candidate
)

from backend.services.nlp_engine import (
    extract_candidate_name,
    extract_resume_sections,
    semantic_project_match
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)

create_table()

create_auth_tables()

create_default_admin()

create_default_requirements()

UPLOAD_FOLDER = "data/resumes"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "message": "HR System Running"
    }


@app.get("/dashboard")
def dashboard():

    return FileResponse(
        "frontend/dashboard.html"
    )


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    valid = verify_admin(
        username,
        password
    )

    if not valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    request.session["admin"] = username

    return {
        "success": True,
        "username": username
    }


@app.post("/logout")
def logout(request: Request):

    request.session.clear()

    return {
        "message": "Logged out"
    }


@app.get("/auth-status")
def auth_status(request: Request):

    admin = request.session.get("admin")

    return {
        "authenticated": bool(admin),
        "username": admin
    }


@app.get("/requirements")
def requirements(request: Request):

    admin = request.session.get("admin")

    if not admin:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return get_requirements()


@app.put("/requirements")
def save_requirements(
    request: Request,
    data: dict
):

    admin = request.session.get("admin")

    if not admin:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    update_requirements(
        data,
        admin
    )

    return {
        "message":
            "Requirements updated successfully"
    }


def extract_text_from_pdf(file_path):

    doc = fitz.open(file_path)

    text = ""

    for page in doc:

        text += page.get_text()

    return text


@app.post("/upload")
def upload_resume(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    extracted_text = extract_text_from_pdf(
        file_path
    )

    candidate_name = extract_candidate_name(
        extracted_text
    )

    sections = extract_resume_sections(
        extracted_text
    )

    project_text = sections.get(
        "projects",
        ""
    )

    requirements = get_requirements()

    semantic_profile = requirements.get(
        "semantic_profile",
        ""
    )

    skills = extract_skills(
        extracted_text
    )

    marks = extract_marks(
        extracted_text
    )

    semantic_result = semantic_project_match(
        sections,
        semantic_profile
    )

    evaluation = evaluate_candidate(
        extracted_text,
        marks,
        skills,
        semantic_result,
        sections
    )

    result = {
        "name": candidate_name,
        "filename": file.filename,
        "skills": skills,
        "marks": marks,
        "semantic_matching":
            semantic_result,
        "sections": {
            "projects":
                project_text[:500]
        },
        "evaluation": evaluation,
        "preview":
            extracted_text[:500]
    }
    print("UPLOAD RESULT:")
    print(result)

    save_candidate(result)

    return result

@app.get("/semantic-search")
def semantic_search(query: str):

    conn = get_connection()

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    sql = text("""
    SELECT
        id,
        name,
        skills,
        score,
        embedding <=> CAST(:embedding AS vector)
        AS distance
    FROM candidates
    ORDER BY distance
    LIMIT 5
    """)

    results = conn.execute(
        sql,
        {
            "embedding":
                str(query_embedding)
        }
    )

    rows = results.fetchall()

    conn.close()

    return [
        dict(row._mapping)
        for row in rows
    ]

@app.get("/demo")
def demo_resume():

    file_path = "data/demo/demo1.pdf"

    extracted_text = extract_text_from_pdf(
        file_path
    )

    candidate_name = extract_candidate_name(
        extracted_text
    )

    sections = extract_resume_sections(
        extracted_text
    )

    project_text = sections.get(
        "projects",
        ""
    )

    requirements = get_requirements()

    semantic_profile = requirements.get(
        "semantic_profile",
        ""
    )

    skills = extract_skills(
        extracted_text
    )

    marks = extract_marks(
        extracted_text
    )

    semantic_result = semantic_project_match(
        sections,
        semantic_profile
    )

    evaluation = evaluate_candidate(
        extracted_text,
        marks,
        skills,
        semantic_result,
        sections
    )

    result = {
        "name": candidate_name,
        "filename": "demo1.pdf",
        "skills": skills,
        "marks": marks,
        "semantic_matching":
            semantic_result,
        "sections": {
            "projects":
                project_text[:500]
        },
        "evaluation": evaluation,
        "preview":
            extracted_text[:500]
    }

    return result


@app.get("/candidates")
def get_candidates():

    conn = get_connection()

    candidates = conn.query(
        Candidate
    ).all()

    conn.close()

    return [
        candidate_to_dict(c)
        for c in candidates
    ]

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "database": "postgresql"
    }