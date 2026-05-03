import streamlit as st
from utils.ml_model import compute_similarity

st.title("💼 Job Matching System (ATS)")

resume_text = st.session_state.get("resume_text", "")

job_desc = st.text_area("Paste Job Description")

if st.button("Match Resume"):

    if resume_text and job_desc:

        score = compute_similarity(resume_text, job_desc)

        st.success(f"ATS Match Score: {score}%")

        if score > 75:
            st.success("Excellent Match 🎯")
        elif score > 50:
            st.warning("Moderate Match ⚡")
        else:
            st.error("Low Match ❌")

    else:
        st.error("Upload resume first")
