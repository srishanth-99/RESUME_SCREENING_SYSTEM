import PyPDF2
import docx

def extract_text(file):
    text = ""

    if file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)

        if pdf_reader.is_encrypted:
            try:
                pdf_reader.decrypt("")
            except:
                return ""

        for page in pdf_reader.pages:
            text += page.extract_text() or ""

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return text
