from fastapi import FastAPI, File, UploadFile
import shutil
import os
import fitz

app = FastAPI()

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
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)

    return {"filename": file.filename, "status": "uploaded", "preview": extracted_text[:500]}