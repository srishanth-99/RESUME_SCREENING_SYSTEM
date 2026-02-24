import base64
import streamlit as st
import requests
from utils.resume_parser import extract_text

# -----------------------------
# Config
# -----------------------------
API_URL = "http://127.0.0.1:8000/analyze"

# -----------------------------
# Background Image
# -----------------------------
def add_bg_image(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image(
    "C://WEB dev//OneDrive//Desktop//resume screening system//assets//bg1.png.jpg"
)

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
                response = requests.post(
                    API_URL,
                    json={"resume_text": resume_text},
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()

                # ❌ Backend validation error
                if "error" in data:
                    st.error(data["error"])
                    st.stop()

                # ✅ Show results
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

                # 📄 Download report
                report_text = generate_report(data)

                st.download_button(
                    label="⬇️ Download Resume Report",
                    data=report_text,
                    file_name="resume_report.txt",
                    mime="text/plain"
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Backend is not running. Please start the FastAPI server."
                )
            except requests.exceptions.Timeout:
                st.error("⏳ Backend took too long to respond.")
            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")
        
