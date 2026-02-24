def calculate_ats(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    matched = resume_words.intersection(jd_words)

    if len(jd_words) == 0:
        return 0

    score = (len(matched) / len(jd_words)) * 100
    return round(score, 2)
