import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("OLLAMA_API_KEY")

print("API KEY LOADED:", bool(api_key))


# Ollama Cloud
client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=api_key
)


def analyze_Resume(resume_text, job_role):

    prompt = f"""
You are HireIQ, an AI-powered resume analyzer.

Analyze this resume for the target job role.

TARGET JOB ROLE:
{job_role}

RESUME:
{resume_text}

Return ONLY a JSON object.

Do NOT use markdown.
Do NOT use ```json.
Do NOT add explanations.

The JSON must have exactly these fields:

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
- missing_skills must contain relevant skills not found in the resume.
- strengths must be supported by the resume.
- weaknesses must identify genuine gaps.
- suggestions must provide practical improvements.
"""


    try:

        response = client.chat.completions.create(
            model="gpt-oss:20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content

        print("\n========== AI RESPONSE ==========")
        print(result)
        print("=================================\n")


        if not result:
            return {
                "error": "AI returned an empty response."
            }


        result = result.strip()


        # Remove markdown if model still adds it
        if result.startswith("```json"):
            result = result[7:]

        elif result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()


        try:
            return json.loads(result)

        except json.JSONDecodeError:

            print("JSON ERROR")
            print("Raw AI response:")
            print(result)

            return {
                "error": "AI returned an invalid JSON response."
            }


    except Exception as e:

        print("OLLAMA ERROR:")
        print(str(e))

        return {
            "error": str(e)
        }