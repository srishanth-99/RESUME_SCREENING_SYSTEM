SKILLS_DB = [
    "python", "java", "sql", "c", "c++", "html", "css", "javascript",
    "machine learning", "deep learning", "data science",
    "flask", "fastapi", "django", "streamlit",
    "power bi", "tableau", "excel"
]

def extract_skills(text):
    text = text.lower()
    found_skills = [skill for skill in SKILLS_DB if skill in text]
    return list(set(found_skills))
