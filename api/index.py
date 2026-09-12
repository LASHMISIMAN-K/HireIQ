from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile

from resume_parser import extract_text
from analyzer import analyze_Resume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def home():
    return {
        "message": "HireIQ API is running 🚀"
    }

@app.post("/api/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_role: str = Form(...)
):
    file_content = await resume.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp:
        temp.write(file_content)
        temp_path = temp.name

    try:
        resume_text = extract_text(temp_path)

        result = analyze_Resume(
            resume_text=resume_text,
            job_role=job_role
        )

        return result

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)