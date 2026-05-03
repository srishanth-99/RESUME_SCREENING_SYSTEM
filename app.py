import streamlit as st
import base64
import os
from utils.resume_parser import extract_text
from backend.skills import extract_skills

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
def add_bg_image():
    BASE_DIR = os.path.dirname(__file__)
    image_path = os.path.join(BASE_DIR, "assets", "bg.png.jpg")  # ✅ your image

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
        st.error(f"❌ Image not found at: {image_path}")

# call background
add_bg_image()

# -----------------------------
# Resume Analysis
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

    # Score
    score = len(detected_skills) * 5

    if "experience" in text:
        score += 30

    if "education" in text:
        score += 20

    score = min(score, 100)

    # Strength
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
    type=["pdf", "docx"]
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
            if st.button("🔍 Analyze Resume"):

                with st.spinner("Analyzing Resume..."):

                    data = analyze_resume(resume_text)

                    st.success("✅ Analysis Complete")

                    st.markdown(f"### 🎯 Predicted Role: **{data['predicted_role']}**")
                    st.markdown(f"### 📊 Resume Score: **{data['resume_score']}%**")
                    st.markdown(f"### 💪 Resume Strength: **{data['resume_strength']}**")

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
