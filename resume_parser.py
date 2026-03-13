import pdfplumber
import docx

def parse_resume(file):

    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    else:
        return ""