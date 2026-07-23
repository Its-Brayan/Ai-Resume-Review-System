# Resume Reviewer
https://ai-resume-review-system.streamlit.app/
A modular AI resume review system built with Streamlit and a graph-based agent workflow.

## Overview

This project provides an interactive resume analysis app that evaluates candidate resumes against job descriptions using multiple AI-driven components.

Key features:
- ATS scoring
- Skills gap analysis
- Resume improvement suggestions
- Career advice
- Final consolidated report generation

The application is driven by a workflow graph in `Workflows/graph.py`, where a Supervisor agent plans the execution path and specialized agents perform each analysis step.

## How it works

1. User uploads a resume (`pdf` or `docx`).
2. User provides a job description either by uploading a file or pasting text.
3. Selected analysis tasks are passed to the workflow.
4. The system extracts text from uploaded documents using `Tools/llama_parser.py`.
5. The workflow executes the requested agents and returns results in the Streamlit UI.

## Project structure

- `app.py` - Streamlit app entry point and user interface.
- `Workflows/graph.py` - Pipeline orchestration and state graph implementation.
- `Agents/` - Contains specialized AI agent modules:
  - `AtsScoringAgent.py`
  - `CareerAdvisorAgent.py`
  - `ReportGeneratorAgent.py`
  - `ResumeImprovementAgent.py`
  - `SkillsGapAgent.py`
  - `SupervisorAgent.py`
- `Tools/` - Document parsing and utility helpers.
- `Config/` - YAML prompt templates used by agents.
- `requirements.txt` - Python dependencies.

## Requirements

- Python 3.10+ (recommended)
- `pip`
- Environment variables for connected AI services

## Setup

1. Clone the repository or download the project files.
2. Create and activate a Python virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the required packages.

```bash
pip install -r requirements.txt
```

4. Set up environment variables.

Create a `.env` file in the project root with the following values:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
LLAMA_API_KEY=your_llama_api_key
```

## Running the app

Start the Streamlit interface with:

```bash
streamlit run app.py
```

Then open the local URL provided by Streamlit in your browser.

## Usage

- Upload a resume file in `pdf` or `docx` format.
- Choose whether to upload a job description file or paste the text directly.
- Select the analyses you want to run:
  - ATS Score
  - Skills Gap Analysis
  - Resume Improvement
  - Career Advice
  - Generate Final Report
- Click `Analyze Resume`.
- Review the generated output sections in the UI.

## Notes

- Document parsing uses the `LlamaCloud` parser in `Tools/llama_parser.py`.
- The workflow is dynamic: the Supervisor agent builds an execution plan based on user-selected tasks.
- `Dockerfile` is currently empty and can be updated later to support containerized deployment.

## Troubleshooting

- If analysis fails, verify that the correct API keys are loaded in the environment.
- Ensure uploaded files are valid `pdf` or `docx` documents.
- If you see import issues, confirm the Python virtual environment is active and dependencies are installed.

