import streamlit as st
import base64
import os
from utils.resume_parser import extract_text
from backend.skills import extract_skills
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI ATS Resume System",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# CUSTOM UI (DARK MODERN THEME)
# -----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

/* Title */
.title {
    font-size: 40px;
    font-weight: 800;
    text-align: center;
    color: #38bdf8;
}

/* Cards */
.card {
    background: #111827;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    margin: 10px 0px;
}

/* Button */
.stButton>button {
    background: #38bdf8;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}

/* File uploader */
.css-1cpxqw2 {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="title">📄 AI Resume Screening & ATS System</div>', unsafe_allow_html=True)
st.write("")

# -----------------------------
# SIDEBAR DASHBOARD
# -----------------------------
st.sidebar.title("📊 Dashboard")
st.sidebar.info("Upload resume to see AI analysis")

# -----------------------------
# ANALYSIS FUNCTION
# -----------------------------
def analyze_resume(text):

    text_lower = text.lower()
    skills = extract_skills(text)

    # ROLE PREDICTION
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

    # SCORE
    score = len(skills) * 10

    if "experience" in text_lower:
        score += 25
    if "education" in text_lower:
        score += 15

    score = min(score, 100)

    if score > 70:
        strength = "Strong 💪"
    elif score > 40:
        strength = "Medium ⚡"
    else:
        strength = "Weak ⚠️"

    return role, score, strength, skills

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("📤 Upload Resume (PDF / DOCX)", type=["pdf", "docx"])

# -----------------------------
# PROCESS
# -----------------------------
if uploaded_file:

    st.success("Resume uploaded successfully ✔")

    with st.spinner("AI analyzing resume... 🤖"):
        text = extract_text(uploaded_file)

    if text:

        role, score, strength, skills = analyze_resume(text)

        # -----------------------------
        # DASHBOARD CARDS
        # -----------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="card">
            <h3>🎯 Predicted Role</h3>
            <h2>{role}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
            <h3>📊 Resume Score</h3>
            <h2>{score}%</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
            <h3>💪 Strength</h3>
            <h2>{strength}</h2>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # -----------------------------
        # SKILL ANALYSIS GRAPH
        # -----------------------------
        st.subheader("📊 Skill Analysis")

        if skills:
            fig, ax = plt.subplots()
            ax.bar(skills, [1]*len(skills))
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("No skills detected")

        # -----------------------------
        # SCORE VISUALIZATION
        # -----------------------------
        st.subheader("📈 Resume Strength Visualization")

        fig2, ax2 = plt.subplots()
        labels = ['Score', 'Remaining']
        values = [score, 100 - score]

        ax2.pie(values, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig2)

        # -----------------------------
        # DOWNLOAD REPORT
        # -----------------------------
        report = f"""
AI RESUME REPORT
================

Role: {role}
Score: {score}%
Strength: {strength}
Skills: {', '.join(skills)}
"""

        st.download_button("⬇ Download Report", report, file_name="resume_report.txt")

    else:
        st.error("Could not extract text from resume")

else:
    st.info("Upload a resume to start AI analysis")
