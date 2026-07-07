from Workflows.graph import run_pipeline
import streamlit as st
from groq import RateLimitError
import traceback
from Tools import easy_ocr,extract_docx,extract_pdf

def extract_text(uploaded_file):
    extension = uploaded_file.name.split(".")[-1].lower()
    if extension == 'pdf':
        return extract_pdf.extract_pdf(uploaded_file)
    elif extension == 'docx':
        return extract_docx.extract_docx(uploaded_file)
    elif extension == 'txt':
        return uploaded_file.read().decode('utf-8')
    elif extension in ['pdf','jpg','jpeg']:
        return easy_ocr(uploaded_file)
    else:
        raise ValueError("Unsupported file type")
st.set_page_config(
    page_title="Resume Analyzer",
    layout='wide'

)
st.title("📄 AI Resume Review System")

st.write("Upload a resume and a job description to receive ATS analysis, "
          "skills matching, resume improvements, and career advice.")

resume = st.file_uploader(
    "Resume",
    type=["pdf", "docx"]
)

job = st.file_uploader(
    "Job description",
    type=['pdf','docx','txt',"txt", "png", "jpg", "jpeg"]
)

def run_async_pipeline(resume,job_description):
    run_pipeline(resume,job_description)

if st.button("Analyze Resume..."):
    if not resume:
        st.warning("Please upload a resume")
        st.stop()
    resume_text = extract_text(resume)
    job_text = extract_text(job)
    # inputs = {
    #     "resume":resume,
    #     "job":job
    # }
    with st.spinner("Analyzing your resume..."):
        try:
            result = run_async_pipeline(resume_text,job_text)
            st.session_state.result = result
        except Exception:
            st.error(f"Error: {traceback.format_exc()} ")


