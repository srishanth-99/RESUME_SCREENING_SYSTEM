import streamlit as st
from utils.resume_parser import extract_text

st.title("📄 Resume Upload")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file:

    text = extract_text(uploaded_file)

    st.success("Resume Loaded ✔")

    st.session_state["resume_text"] = text

    st.text_area("Extracted Text", text, height=300)
