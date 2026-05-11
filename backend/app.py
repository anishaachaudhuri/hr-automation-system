from fastapi import FastAPI, File, UploadFile
import shutil
import os
import fitz

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

app = FastAPI()

# create database table on startup
create_table()

UPLOAD_FOLDER = "data/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "HR System Running"}


def extract_text_from_pdf(file_path):

    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


@app.post("/upload")
def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # extract text
    extracted_text = extract_text_from_pdf(file_path)

    # extract skills and marks
    skills = extract_skills(extracted_text)
    marks = extract_marks(extracted_text)

    # evaluate candidate
    evaluation = evaluate_candidate(extracted_text, marks)

    # create final result object
    result = {
        "filename": file.filename,
        "skills": skills,
        "marks": marks,
        "evaluation": evaluation,
        "preview": extracted_text[:500]
    }

    # save candidate to database
    save_candidate(result)

    return result


@app.get("/demo")
def demo_resume():

    file_path = "data/demo/demo1.pdf"

    extracted_text = extract_text_from_pdf(file_path)

    skills = extract_skills(extracted_text)
    marks = extract_marks(extracted_text)

    evaluation = evaluate_candidate(extracted_text, marks)

    result = {
        "filename": "demo1.pdf",
        "skills": skills,
        "marks": marks,
        "evaluation": evaluation,
        "preview": extracted_text[:300]
    }

    return result


@app.get("/candidates")
def get_candidates():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")

    candidates = cursor.fetchall()

    conn.close()

    return [dict(candidate) for candidate in candidates]