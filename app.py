import base64
import streamlit as st
from utils.resume_parser import extract_text

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

# If image exists in assets folder
add_bg_image("assets/bg1.png.jpg")

# -----------------------------
# Skill Keywords
# -----------------------------
SKILLS_DB = [
    "python", "java", "c++", "sql",
    "machine learning", "data analysis",
    "power bi", "excel", "tableau",
    "deep learning", "html", "css"
]

# -----------------------------
# Streamlit UI
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

        resume_text_lower = resume_text.lower()

        # Extract Skills
        found_skills = []
        for skill in SKILLS_DB:
            if skill in resume_text_lower:
                found_skills.append(skill.title())

        # Basic Score Logic
        resume_score = min(len(found_skills) * 10, 100)

        # Predicted Role Logic
        if "machine learning" in resume_text_lower or "deep learning" in resume_text_lower:
            predicted_role = "Machine Learning Engineer"
        elif "power bi" in resume_text_lower or "tableau" in resume_text_lower:
            predicted_role = "Business Intelligence Analyst"
        elif "python" in resume_text_lower or "sql" in resume_text_lower:
            predicted_role = "Data Analyst"
        else:
            predicted_role = "General Candidate"

        # Strength
        if resume_score >= 70:
            resume_strength = "Strong"
        elif resume_score >= 40:
            resume_strength = "Moderate"
        else:
            resume_strength = "Needs Improvement"

        # -----------------------------
        # Display Results
        # -----------------------------
        st.success("✅ Resume analyzed successfully")

        st.markdown(f"### 🎯 Predicted Role: **{predicted_role}**")
        st.markdown(f"### 📊 Resume Quality Score: **{resume_score}%**")
        st.markdown(f"### 📌 Resume Strength: **{resume_strength}**")

        st.markdown("### 🛠 Extracted Skills")
        if found_skills:
            st.write(", ".join(found_skills))
        else:
            st.write("No major skills detected.")