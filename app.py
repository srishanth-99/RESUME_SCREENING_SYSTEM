import streamlit as st
import base64
import os
from utils.resume_parser import extract_text

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="centered"
)

# -----------------------------
# Background Image
# -----------------------------
def add_bg_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}

            .block-container {{
                background-color: rgba(255,255,255,0.9);
                padding: 2rem;
                border-radius: 10px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Background image not found.")

add_bg_image("assets/bg1.png")

# -----------------------------
# Skill Detection + Role Prediction
# -----------------------------
def analyze_resume(resume_text):

    skills_db = [
        "python","sql","excel","machine learning","data analysis",
        "tableau","power bi","java","c++","html","css","javascript",
        "deep learning","nlp","pandas","numpy","tensorflow"
    ]

    detected_skills = []
    text = resume_text.lower()

    for skill in skills_db:
        if skill in text:
            detected_skills.append(skill.title())

    # -----------------------------
    # Role Prediction
    # -----------------------------
    if "machine learning" in text or "deep learning" in text:
        role = "Machine Learning Engineer"

    elif "python" in text and "sql" in text:
        role = "Data Analyst"

    elif "html" in text or "css" in text or "javascript" in text:
        role = "Web Developer"

    elif "java" in text or "c++" in text:
        role = "Software Developer"

    else:
        role = "General IT Role"

    # -----------------------------
    # Resume Score
    # -----------------------------
    score = min(len(detected_skills) * 10, 100)

    if score > 70:
        strength = "Strong"
    elif score > 40:
        strength = "Average"
    else:
        strength = "Weak"

    return {
        "predicted_role": role,
        "resume_score": score,
        "resume_strength": strength,
        "skills": detected_skills
    }

# -----------------------------
# Report Generator
# -----------------------------
def generate_report(data):

    return f"""
RESUME SCREENING REPORT
======================

Predicted Role:
{data['predicted_role']}

Resume Quality Score:
{data['resume_score']}%

Resume Strength:
{data['resume_strength']}

Extracted Skills:
{', '.join(data['skills'])}
"""

# -----------------------------
# UI
# -----------------------------
st.title("📄 Resume Screening System")

st.info("📌 Upload a resume in PDF or DOCX format")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf","docx"]
)

# -----------------------------
# PROCESS RESUME
# -----------------------------
if uploaded_file:

    st.success("✅ Resume Uploaded Successfully")

    try:
        resume_text = extract_text(uploaded_file)

        if not resume_text:
            st.error("⚠️ Unable to extract text from resume")

        else:

            if st.button("Analyze Resume"):

                with st.spinner("🔍 Analyzing Resume..."):

                    data = analyze_resume(resume_text)

                    st.success("✅ Analysis Complete")

                    st.markdown(
                        f"### 🎯 Predicted Role: **{data['predicted_role']}**"
                    )

                    st.markdown(
                        f"### 📊 Resume Score: **{data['resume_score']}%**"
                    )

                    st.markdown(
                        f"### 💪 Resume Strength: **{data['resume_strength']}**"
                    )

                    st.markdown("### 🛠 Detected Skills")

                    if data["skills"]:
                        st.write(", ".join(data["skills"]))
                    else:
                        st.write("No skills detected")

                    report_text = generate_report(data)

                    st.download_button(
                        label="⬇ Download Report",
                        data=report_text,
                        file_name="resume_report.txt",
                        mime="text/plain"
                    )

    except Exception as e:
        st.error(f"⚠️ Error processing resume: {e}")
