from Workflows.graph import run_pipeline
import streamlit as st
# from groq import RateLimitError
import traceback
from Tools.GeminiDocumentParser import GeminiDocumentParser

parser = GeminiDocumentParser()
# from Tools.extract_pdf import extract_pdf
# from Tools.extract_docx import extract_docx


# def extract_text(uploaded_file):
#     extension = uploaded_file.name.split(".")[-1].lower()
#     if extension == 'pdf':
#         return extract_pdf(uploaded_file)
#     elif extension == 'docx':
#         return extract_docx(uploaded_file)
#     elif extension == 'txt':
#         return uploaded_file.read().decode('utf-8')
#     elif extension in ['png','jpg','jpeg']:
#         from Tools.easy_ocr import extract_text_from_image
#         return extract_text_from_image(uploaded_file)
#     else:
#         raise ValueError("Unsupported file type")

if "result" not in st.session_state:
    st.session_state.result = None

st.set_page_config(
    page_title="Resume Analyzer",
    layout='wide'

)
st.title("📄 AI Resume Review System")

st.write("Upload a resume and a job description to receive ATS analysis, "
          "skills matching, resume improvements, and career advice.")

resume_file = st.file_uploader(
    "Resume",
    type=["pdf", "docx"]
)

job_input_method = st.radio(
    "Choose how to provide the job description:",
    ["Upload File", "Paste Text"]
)
st.subheader("Choose the analyses you want")

ats = st.checkbox("ATS Score")
skills = st.checkbox("Skills Gap Analysis")
resume_improvement = st.checkbox("Resume Improvement")
career = st.checkbox("Career Advice")
report = st.checkbox("Generate Final Report", value=True)

selected_tasks = []

if ats:
    selected_tasks.append("ats_scorer")

if skills:
    selected_tasks.append("skills_checker")

if resume_improvement:
    selected_tasks.append("resume_improver")

if career:
    selected_tasks.append("career_advisor")

if report:
    selected_tasks.append("final_report")

def run_async_pipeline(resume,job_description,selected_tasks):
    return run_pipeline(resume,job_description,selected_tasks)
job = None
job_text = ""
if job_input_method == "Upload File":
     job = st.file_uploader(
     "Job description",
     type=['pdf','docx','txt',"txt", "png", "jpg", "jpeg"]
        )
elif job_input_method == "Paste Text":
        job_text = st.text_area(
        "Paste the Job Description",
        height=300,
        placeholder="Paste the complete job description here..."
        )
if st.button("Analyze Resume"):
    if not resume_file:
        st.warning("Please upload a resume")
        st.stop()
    resume_text = parser.parse_resume(resume_file)

    if job_input_method == "Upload File":
        if job is None:
            st.warning("Please upload a job description")
            st.stop()
        job_text = parser.parse_job(job)
    else:
        if not job_text.strip():
         st.warning("Please paste a job description.")
         st.stop()

    # inputs = {
    #     "resume":resume,
    #     "job":job
    # }
    with st.spinner("Analyzing your resume..."):
        try:
            result = run_async_pipeline(resume_text,job_text,selected_tasks)
            st.session_state.result = result
        except Exception:
            st.error(f"Error: {traceback.format_exc()} ")



if st.session_state.result:

    res = st.session_state.result
    st.markdown("### 🧭 Overview")

    
    st.markdown(res.get("resume_parser", ""))

    # 2. Clean sections only
    st.markdown("### 🏨 Job Analyzer")
    st.markdown(res.get("job_analyzer", ""))

    st.markdown("### 💰 ATS Scorer")
    st.markdown(res.get("ats_scorer", ""))

    st.markdown("### 🗺️ Resume Improver")
    st.markdown(res.get("resume_improver", ""))
    
    st.markdown("### Career Advice")
    st.markdown(res.get('career_advice', ""))

    st.markdown("### Final Report")
    st.markdown(res.get('final_report'))
    
