from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)


from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

import tempfile
import os

from backend.resume_parser import extract_text
from backend.analyzer import analyze_Resume
from backend.database import create_database, get_connection

from backend.auth import (
    hash_password,
    verify_password,
    create_token,
    get_current_user
)


load_dotenv()


app = FastAPI(
    title="HireIQ API"
)

BASE_DIR = Path(__file__).resolve().parent.parent


@app.get("/")
def frontend():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/style.css")
def css():
    return FileResponse(BASE_DIR / "style.css")


@app.get("/script.js")
def javascript():
    return FileResponse(BASE_DIR / "script.js")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


create_database()


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/api/")
def home():

    return {
        "message": "HireIQ API is running 🚀"
    }


# -------------------------
# REGISTER
# -------------------------

@app.post("/api/register")
def register(data: RegisterRequest):

    name = data.name.strip()
    email = data.email.strip().lower()


    if len(data.password) < 6:

        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 6 characters"
        )


    conn = get_connection()

    existing = conn.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()


    if existing:

        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    hashed = hash_password(
        data.password
    )


    cursor = conn.execute(
        """
        INSERT INTO users
        (name, email, password)
        VALUES (?, ?, ?)
        """,
        (
            name,
            email,
            hashed
        )
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()


    token = create_token(
        user_id
    )


    return {
        "message": "Account created successfully",
        "token": token
    }


# -------------------------
# LOGIN
# -------------------------

@app.post("/api/login")
def login(data: LoginRequest):

    conn = get_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (
            data.email.strip().lower(),
        )
    ).fetchone()

    conn.close()


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    if not verify_password(
        data.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_token(
        user["id"]
    )


    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }


# -------------------------
# CURRENT USER
# -------------------------

@app.get("/api/me")
def me(
    user=Depends(get_current_user)
):

    return user


# -------------------------
# PROTECTED ANALYZER
# -------------------------

@app.post("/api/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_role: str = Form(...),
    user=Depends(get_current_user)
):

    if not resume.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume"
        )


    content = await resume.read()

    temp_path = None


    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp:

            temp.write(content)

            temp_path = temp.name


        resume_text = extract_text(
            temp_path
        )


        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF"
            )


        result = analyze_Resume(
            resume_text,
            job_role
        )


        return result


    finally:

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            os.remove(temp_path)