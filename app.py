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
    page_title="AI Resume ATS System",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# UI STYLE
# -----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

.title {
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    color: #38bdf8;
}

.card {
    background: #111827;
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}

.stButton>button {
    background: #38bdf8;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 45px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="title">📄 AI Resume Screening & ATS System</div>', unsafe_allow_html=True)

# -----------------------------
# SIDEBAR DASHBOARD (FIXED)
# -----------------------------
st.sidebar.title("📊 Dashboard")

uploaded_file = st.file_uploader("📤 Upload Resume (PDF / DOCX)", type=["pdf", "docx"])

if uploaded_file:
    st.sidebar.success("Resume Uploaded ✔")
else:
    st.sidebar.warning("No Resume Uploaded ❌")

st.sidebar.markdown("---")
st.sidebar.write("✔ Role Prediction")
st.sidebar.write("✔ Skill Extraction")
st.sidebar.write("✔ AI Scoring")
st.sidebar.write("✔ Download Report")

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

    # SCORE (REALISTIC)
    score = min(len(skills) * 12, 70)

    if "experience" in text_lower:
        score += 15
    if "education" in text_lower:
        score += 10

    score = min(score, 100)

    # STRENGTH
    if score > 70:
        strength = "Strong 💪"
    elif score > 40:
        strength = "Medium ⚡"
    else:
        strength = "Weak ⚠️"

    return role, score, strength, skills

# -----------------------------
# PROCESS RESUME
# -----------------------------
if uploaded_file:

    st.success("Resume uploaded successfully ✔")

    with st.spinner("AI analyzing resume... 🤖"):
        text = extract_text(uploaded_file)

    if text:

        role, score, strength, skills = analyze_resume(text)

        # -----------------------------
        # METRICS DASHBOARD (FIXED)
        # -----------------------------
        st.subheader("📊 Dashboard Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("🎯 Predicted Role", role)
        col2.metric("📊 Score", f"{score}%")
        col3.metric("💪 Strength", strength)

        st.write("---")

        # -----------------------------
        # SKILLS GRAPH (FIXED)
        # -----------------------------
        st.subheader("📊 Skill Analysis")

        if skills and len(skills) > 0:

            unique_skills = list(set(skills))

            fig, ax = plt.subplots()
            ax.bar(unique_skills, [1] * len(unique_skills))
            plt.xticks(rotation=45)

            st.pyplot(fig)

        else:
            st.warning("⚠️ No skills detected")

        # -----------------------------
        # PIE CHART
        # -----------------------------
        st.subheader("📈 Score Visualization")

        fig2, ax2 = plt.subplots()
        ax2.pie(
            [score, 100 - score],
            labels=["Score", "Remaining"],
            autopct="%1.1f%%"
        )
        st.pyplot(fig2)

        # -----------------------------
        # REPORT
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
    st.info("👆 Upload a resume to start AI analysis")
