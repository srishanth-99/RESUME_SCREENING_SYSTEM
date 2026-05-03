import streamlit as st
import base64
import os
import matplotlib.pyplot as plt

from utils.resume_parser import extract_text
from backend.skills import extract_skills

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="centered"
)

# -----------------------------
# PROFESSIONAL UI STYLING
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}

h1, h2, h3 {
    color: white;
    text-align: center;
}

.block-container {
    background-color: rgba(255,255,255,0.92);
    padding: 2rem;
    border-radius: 15px;
    color: black;
}

.stButton>button {
    background-color: #00c6ff;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# BACKGROUND IMAGE (optional)
# -----------------------------
def add_bg_image():
    image_path = os.path.join("assets", "bg1.png.jpg")

    if os.path.exists(image_path):
        with open(image_path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

add_bg_image()

# -----------------------------
# RESUME ANALYSIS FUNCTION
# -----------------------------
def analyze_resume(resume_text):
    text = resume_text.lower()
    detected_skills = extract_skills(resume_text)

    # Role prediction
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

    # Score calculation
    score = len(detected_skills) * 5

    if "experience" in text:
        score += 30
    if "education" in text:
        score += 20

    score = min(score, 100)

    strength = "Strong 💪" if score > 70 else "Average 🙂" if score > 40 else "Weak ⚠️"

    return {
        "predicted_role": role,
        "resume_score": score,
        "resume_strength": strength,
        "skills": detected_skills
    }

# -----------------------------
# REPORT GENERATOR
# -----------------------------
def generate_report(data):
    return f"""
RESUME SCREENING REPORT
======================

Predicted Role: {data['predicted_role']}
Resume Score: {data['resume_score']}%
Strength: {data['resume_strength']}
Skills: {', '.join(data['skills'])}
"""

# -----------------------------
# DASHBOARD
# -----------------------------
def show_dashboard(score, skills):
    st.subheader("📊 Skill Analysis Dashboard")

    labels = ["Skills Found", "Missing Skills"]
    values = [len(skills), max(10 - len(skills), 0)]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    ax.set_title("Resume Skill Distribution")

    st.pyplot(fig)

    st.subheader("📈 Resume Score Progress")
    st.progress(score / 100)

# -----------------------------
# UI HEADER
# -----------------------------
st.title("📄 AI Resume Screening System")
st.write("Upload your resume and get AI-powered analysis")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF / DOCX)",
    type=["pdf", "docx"]
)

# -----------------------------
# PROCESS
# -----------------------------
if uploaded_file:

    st.success("✅ Resume Uploaded Successfully")

    try:
        resume_text = extract_text(uploaded_file)

        if resume_text:

            if st.button("🔍 Analyze Resume"):

                with st.spinner("Analyzing Resume... 🤖"):

                    data = analyze_resume(resume_text)

                    st.success("✅ Analysis Complete")

                    # RESULTS
                    st.markdown(f"### 🎯 Predicted Role: **{data['predicted_role']}**")
                    st.markdown(f"### 📊 Score: **{data['resume_score']}%**")
                    st.markdown(f"### 💪 Strength: **{data['resume_strength']}**")

                    st.markdown("### 🛠 Skills Detected")
                    st.write(", ".join(data["skills"]) if data["skills"] else "No skills found")

                    # DASHBOARD (IMPORTANT)
                    show_dashboard(data["resume_score"], data["skills"])

                    # DOWNLOAD REPORT
                    report = generate_report(data)

                    st.download_button(
                        label="⬇ Download Report",
                        data=report,
                        file_name="resume_report.txt",
                        mime="text/plain"
                    )

        else:
            st.error("⚠️ Could not extract text from resume")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
