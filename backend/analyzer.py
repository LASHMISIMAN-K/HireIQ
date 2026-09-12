import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

print("GEMINI API KEY LOADED:", bool(api_key))

client = genai.Client(api_key=api_key)


def analyze_Resume(resume_text, job_role):

    prompt = f"""
You are HireIQ, an AI-powered resume analyzer.

Analyze this resume for the target job role.

TARGET JOB ROLE:
{job_role}

RESUME:
{resume_text}

Analyze the candidate specifically for the target job role.

Return the result as JSON with exactly these fields:

{{
    "ats_score": 0,
    "summary": "",
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": []
}}

Rules:

- ats_score must be an integer between 0 and 100.
- matched_skills must contain skills actually found in the resume.
- missing_skills must contain relevant skills required or commonly expected for the target role but not found in the resume.
- strengths must be supported by the resume.
- weaknesses must identify genuine gaps.
- suggestions must provide practical improvements.
- Be realistic and specific.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json"
            )
        )

        result = response.text

        print("\n========== GEMINI RESPONSE ==========")
        print(result)
        print("=====================================\n")

        if not result:
            return {
                "error": "Gemini returned an empty response."
            }

        return json.loads(result)

    except Exception as e:

        print("GEMINI ERROR:")
        print(str(e))

        return {
            "error": str(e)
        }