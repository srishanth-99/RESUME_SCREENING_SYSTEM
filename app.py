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
    layout="centered"
)

# -----------------------------
# MODERN UI STYLING
# -----------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #eef2f3, #dfe9f3);
    font-family: 'Arial';
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #2C3E50;
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: gray;
    font-size: 16px;
    margin-bottom: 20px;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

/* Buttons */
.stButton>button {
    background-color: #4A90E2;
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-weight: bold;
}

/* Success box */
.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='main-title'>📄 AI Resume Screening System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Upload your resume and get instant AI-powered analysis</div>", unsafe_allow_html=True)

# -----------------------------
# FILE UPLOAD CARD
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📤 Upload your Resume (PDF / DOCX)",
    type=["pdf", "docx"]
)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# RESUME ANALYSIS FUNCTION
# -----------------------------
def analyze_resume(resume_text):

    text = resume_text.lower()
    detected_skills = extract_skills(resume_text)

    if "machine learning" in text or "deep learning" in text:
        role = "Machine Learning Engineer"
    elif "python" in text and "sql" in text:
        role = "Data Analyst"
    elif any(x in text for x in ["html", "css", "javascript"]):
        role = "Web Developer"
    elif any(x in text for x in ["java", "c++"]):
        role = "Software Developer"
    else:
        role = "General IT Role"

    score = len(detected_skills) * 5

    if "experience" in text:
        score += 30
    if "education" in text:
        score += 20

    score = min(score, 100)

    strength = "Strong" if score > 70 else "Average" if score > 40 else "Weak"

    return {
        "role": role,
        "score": score,
        "strength": strength,
        "skills": detected_skills
    }

# -----------------------------
# REPORT
# -----------------------------
def generate_report(data):
    return f"""
AI RESUME REPORT
====================

Predicted Role: {data['role']}
Score: {data['score']}%
Strength: {data['strength']}

Skills: {', '.join(data['skills'])}
"""

# -----------------------------
# PROCESS
# -----------------------------
if uploaded_file:

    st.success("✅ Resume uploaded successfully!")

    try:
        resume_text = extract_text(uploaded_file)

        if st.button("🚀 Analyze Resume"):

            with st.spinner("🤖 AI is analyzing your resume..."):
                import time
                time.sleep(2)

                data = analyze_resume(resume_text)

            st.success("🎉 Analysis Complete!")

            # ---------------- RESULTS ----------------
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.markdown(f"### 🎯 Predicted Role: **{data['role']}**")
            st.markdown(f"### 📊 Score: **{data['score']}%**")
            st.markdown(f"### 💪 Strength: **{data['strength']}**")

            st.markdown("### 🛠 Skills Detected")
            st.write(", ".join(data['skills']) if data['skills'] else "No skills found")

            st.markdown("</div>", unsafe_allow_html=True)

            # ---------------- DOWNLOAD ----------------
            report = generate_report(data)

            st.download_button(
                "⬇ Download Report",
                report,
                file_name="resume_report.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
