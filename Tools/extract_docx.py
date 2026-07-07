from docx import Document

def extract_docx(uploaded_file):
    document = Document(uploaded_file)

    return "/n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )
