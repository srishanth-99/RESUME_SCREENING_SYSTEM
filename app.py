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
# SAFE Background Image
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
                background-color: rgba(255, 255, 255, 0.90);
                padding: 2rem;
                border-radius: 12px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Background image not found. Check assets folder.")

# Change filename if needed
add_bg_image("assets/bg1.png")

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
st.info("📌 Upload only a valid resume in PDF or DOCX format.")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF / DOCX only)",
    type=["pdf", "docx"]
)

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    if st.button("Analyze Resume"):

        with st.spinner("🔍 Analyzing resume..."):

            try:
                # 🔥 Dummy Prediction (Replace later with ML model)
                data = {
                    "predicted_role": "Data Analyst",
                    "resume_score": 85,
                    "resume_strength": "Strong",
                    "skills": ["Python", "SQL", "Machine Learning", "Excel"]
                }

                st.success("✅ Resume analyzed successfully")

                st.markdown(
                    f"### 🎯 Predicted Role: **{data['predicted_role']}**"
                )
                st.markdown(
                    f"### 📊 Resume Quality Score: **{data['resume_score']}%**"
                )
                st.markdown(
                    f"### 📌 Resume Strength: **{data['resume_strength']}**"
                )

                st.markdown("### 🛠 Extracted Skills")
                st.write(", ".join(data["skills"]))

                # Download Report
                report_text = generate_report(data)

                st.download_button(
                    label="⬇️ Download Resume Report",
                    data=report_text,
                    file_name="resume_report.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
