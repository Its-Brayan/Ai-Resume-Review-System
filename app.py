from Workflows.graph import run_pipeline
import streamlit as st
from groq import RateLimitError
import traceback
from Tools.extract_pdf import extract_pdf
from Tools.extract_docx import extract_docx


def extract_text(uploaded_file):
    extension = uploaded_file.name.split(".")[-1].lower()
    if extension == 'pdf':
        return extract_pdf(uploaded_file)
    elif extension == 'docx':
        return extract_docx(uploaded_file)
    elif extension == 'txt':
        return uploaded_file.read().decode('utf-8')
    elif extension in ['png','jpg','jpeg']:
        from Tools.easy_ocr import extract_text_from_image
        return extract_text_from_image(uploaded_file)
    else:
        raise ValueError("Unsupported file type")

if "result" not in st.session_state:
    st.session_state.result = None

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
    return run_pipeline(resume,job_description)

if st.button("Analyze Resume"):
    if not resume:
        st.warning("Please upload a resume")
        st.stop()
    resume_text = extract_text(resume)
    job_text  = ''
    if job is not None:

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



if st.session_state.result:

    res = st.session_state.result
    st.markdown("### 🧭 Overview")
    st.markdown(res.get("parser", ""))

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
    
