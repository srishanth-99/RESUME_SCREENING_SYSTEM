from fastapi import FastAPI
from pydantic import BaseModel
import re
from typing import List

app = FastAPI(title="Resume Screening API")

# -----------------------------
# Request Model
# -----------------------------
class ResumeRequest(BaseModel):
    resume_text: str


# -----------------------------
# Resume Validation Logic
# -----------------------------
def is_resume(text: str) -> bool:
    if not text:
        return False

    text = text.lower()

    resume_keywords = [
        "education", "skills", "experience", "projects",
        "internship", "certification", "objective",
        "summary", "work experience", "technical skills"
    ]

    keyword_count = sum(1 for k in resume_keywords if k in text)

    email_found = bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text))
    phone_found = bool(re.search(r"\b\d{10}\b", text))

    if len(text) < 300:
        return False
    if keyword_count < 2:
        return False
    if not (email_found or phone_found):
        return False

    return True


# -----------------------------
# Dummy Analysis Functions
# -----------------------------
def extract_skills(text: str) -> List[str]:
    skills_db = [
        "python", "java", "sql", "power bi", "tableau",
        "machine learning", "excel", "html", "css"
    ]
    return [s for s in skills_db if s in text.lower()]


def predict_role(skills: List[str]) -> str:
    if "python" in skills and "machine learning" in skills:
        return "Data Scientist"
    if "sql" in skills and "power bi" in skills:
        return "Data Analyst"
    if "java" in skills:
        return "Java Developer"
    return "Software Engineer"


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/analyze")
def analyze_resume(data: ResumeRequest):
    resume_text = data.resume_text

    # ❌ Reject if not a resume
    if not is_resume(resume_text):
        return {
            "error": "❌ The uploaded file is NOT a valid resume. Please upload a proper resume (PDF or DOCX only)."
        }

    # ✅ Resume accepted
    skills = extract_skills(resume_text)
    role = predict_role(skills)

    resume_score = min(100, 50 + len(skills) * 8)
    strength = "Strong" if resume_score >= 75 else "Moderate" if resume_score >= 60 else "Weak"

    return {
        "predicted_role": role,
        "resume_score": resume_score,
        "resume_strength": strength,
        "skills": skills
    }
