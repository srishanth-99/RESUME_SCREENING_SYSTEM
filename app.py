import streamlit as st
import base64
import os
from utils.resume_parser import extract_text
from backend.skills import extract_skills

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (PRO UI)
# -----------------------------
st.markdown("""
<style>

body {
    background-color: #0f172a;
}

.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
}

/* Title */
.title {
    font-size: 42px;
    font-weight: 800;
    color: #38bdf8;
    text-align: center;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
    margin-top: 10px;
}

/* Buttons */
.stButton>button {
    background-color: #38bdf8;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="title">📄 AI Resume Screening System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your resume and get instant AI analysis 🚀</div>', unsafe_allow_html=True)

st.write("")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("📤 Upload Resume (PDF / DOCX)", type=["pdf", "docx"])

# -----------------------------
# ANALYSIS FUNCTION
# -----------------------------
def analyze_resume(text):

    text_lower = text.lower()
    skills = extract_skills(text)

    if "machine learning" in text_lower:
        role = "Machine Learning Engineer"
    elif "python" in text_lower and "sql" in text_lower:
        role = "Data Analyst"
    elif "html" in text_lower or "css" in text_lower:
        role = "Web Developer"
    elif "java" in text_lower:
        role = "Software Developer"
    else:
        role = "General IT Role"

    score = len(skills) * 8

    if "experience" in text_lower:
        score += 25
    if "education" in text_lower:
        score += 20

    score = min(score, 100)

    if score > 70:
        strength = "Strong 💪"
    elif score > 40:
        strength = "Medium ⚡"
    else:
        strength = "Weak ⚠️"

    return role, score, strength, skills

# -----------------------------
# PROCESS
# -----------------------------
if uploaded_file:

    st.success("File uploaded successfully ✔")

    with st.spinner("🤖 AI is analyzing your resume..."):
        text = extract_text(uploaded_file)

    if text:

        role, score, strength, skills = analyze_resume(text)

        st.markdown("## 📊 Analysis Report")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='card'><h3>🎯 Role</h3><p>{role}</p></div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='card'><h3>📈 Score</h3><p>{score}%</p></div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='card'><h3>💪 Strength</h3><p>{strength}</p></div>", unsafe_allow_html=True)

        st.write("")

        st.markdown("## 🛠 Skills Found")
        if skills:
            st.success(", ".join(skills))
        else:
            st.warning("No skills detected")

        # Download Report
        report = f"""
Resume Report

Role: {role}
Score: {score}%
Strength: {strength}
Skills: {', '.join(skills)}
"""

        st.download_button("⬇ Download Report", report, file_name="resume_report.txt")

    else:
        st.error("Could not read resume text")

else:
    st.info("👆 Upload a resume to start analysis")
