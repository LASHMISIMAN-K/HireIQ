HireIQ

HireIQ is an AI-powered resume analyzer that helps job seekers understand how well their resume matches a target job role. It extracts text from PDF resumes and uses Google Gemini AI to generate an ATS-style score, matched skills, missing skills, strengths, weaknesses, and practical improvement suggestions.

Features

PDF resume upload

Target job role matching

AI-powered resume analysis

ATS-style score from 0–100

Matched and missing skills

Resume strengths and weaknesses

Actionable improvement suggestions

User registration and login

JWT authentication

Argon2 password hashing

Glassmorphism UI

FastAPI backend

Vercel deployment support

Tech Stack

Frontend

HTML5

CSS3

JavaScript

Backend

Python

FastAPI

Uvicorn

PyPDF

AI

Google Gemini API

Google GenAI SDK

Authentication

PyJWT

pwdlib

Argon2

Database

SQLite for local development

PostgreSQL recommended for production

Deployment

Vercel

Project Structure

HireIQ/
├── api/
│   └── index.py
├── backend/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   └── resume_parser.py
├── index.html
├── style.css
├── script.js
├── requirements.txt
├── vercel.json
├── .env
└── .gitignore

How It Works

User
  ↓
Register / Login
  ↓
JWT Authentication
  ↓
HireIQ Dashboard
  ↓
Enter Target Job Role + Upload Resume
  ↓
FastAPI Backend
  ↓
Extract Resume Text
  ↓
Google Gemini AI
  ↓
ATS Score + Skills + Strengths + Weaknesses + Suggestions

Installation

1. Clone the repository

git clone https://github.com/LASHMISIMAN-K/HireIQ.git
cd HireIQ

2. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

Environment Variables

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET_KEY=your_jwt_secret

Generate a secure JWT secret:

python -c "import secrets; print(secrets.token_urlsafe(64))"

Never commit .env or expose API keys in frontend code.

Run Locally

From the project root:

uvicorn backend.main:app --reload

The API will run at:

http://127.0.0.1:8000

API Endpoints

Health Check

GET /api/

Register

POST /api/register

Example:

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}

Login

POST /api/login

Current User

GET /api/me

Requires:

Authorization: Bearer <JWT_TOKEN>

Resume Analysis

POST /api/analyze

Requires a JWT token and multipart form data:

resume: resume.pdf
job_role: Frontend Developer

Example AI Response

{
  "ats_score": 82,
  "summary": "The resume is well aligned with the target role.",
  "matched_skills": [
    "HTML",
    "CSS",
    "JavaScript",
    "React"
  ],
  "missing_skills": [
    "TypeScript",
    "Testing"
  ],
  "strengths": [
    "Strong frontend development skills"
  ],
  "weaknesses": [
    "Limited testing experience"
  ],
  "suggestions": [
    "Add TypeScript projects",
    "Include testing experience"
  ]
}

Authentication & Security

HireIQ uses JWT authentication to protect user-specific endpoints.

Passwords are hashed using Argon2 before being stored. Plain-text passwords are not stored.

Keep these secrets private:

GEMINI_API_KEY
JWT_SECRET_KEY

Recommended .gitignore entries:

.env
hireiq.db
__pycache__/
*.pyc

Database

The development version uses SQLite.

For production deployment on Vercel, use a persistent hosted PostgreSQL database instead of SQLite.

Deployment

HireIQ uses the FastAPI entry point:

api/index.py

The entry point contains:

from backend.main import app

Set the Vercel root directory to:

./

Add these environment variables in Vercel:

GEMINI_API_KEY
JWT_SECRET_KEY

For the current setup:

{}

can be used as vercel.json.

Future Improvements

PostgreSQL production database

Resume history

Job description analysis

Resume-to-job compatibility score

Resume keyword optimization

AI-powered resume improvement

Cover letter generation

Job recommendations

LinkedIn profile analysis

Resume PDF report generation

User profile management

Analytics dashboard

Use Case

HireIQ is designed for students, fresh graduates, and job seekers who want to evaluate their resume before applying for a job.

Resume + Target Job Role
          ↓
       HireIQ AI
          ↓
      ATS Score
          ↓
Matched / Missing Skills
          ↓
Strengths / Weaknesses
          ↓
Improvement Suggestions

Author

LASHMISIMAN K

B.Tech — Computer Science Engineering
IoT and Automation

GitHub: https://github.com/LASHMISIMAN-K

License

This project is currently intended for educational and development purposes.