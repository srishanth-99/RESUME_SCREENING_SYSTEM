import streamlit as st
from utils.ml_model import compute_similarity

st.title("🏆 Resume Ranking Leaderboard")

job_desc = st.text_area("Paste Job Description")

uploaded_files = st.file_uploader(
    "Upload Multiple Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

results = []

if st.button("Rank Resumes"):

    for file in uploaded_files:

        from utils.resume_parser import extract_text
        text = extract_text(file)

        score = compute_similarity(text, job_desc)

        results.append((file.name, score))

    results.sort(key=lambda x: x[1], reverse=True)

    for name, score in results:

        st.write(f"📄 {name} → {score}%")
