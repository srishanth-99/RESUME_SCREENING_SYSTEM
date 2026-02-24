# backend/matcher.py

def job_match_percentage(resume_text, jd_text):
    resume_set = set(resume_text.lower().split())
    jd_set = set(jd_text.lower().split())

    if not jd_set:
        return 0.0

    match = resume_set.intersection(jd_set)
    return round((len(match) / len(jd_set)) * 100, 2)

