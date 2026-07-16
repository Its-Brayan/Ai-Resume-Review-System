import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class GeminiDocumentParser:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise RuntimeError('GEMINI_API_KEY is not set in the environment.')
        self.client = genai.Client(api_key=api_key)

    def _build_file_part(self, uploaded_file):
        mime_type = getattr(uploaded_file, 'type', None) or 'application/octet-stream'
        return types.Part.from_bytes(
            data=uploaded_file.read(),
            mime_type=mime_type
        )

    def _clean_text(self, text: str) -> str:
        return text.replace('```json', '').replace('```', '').strip()

    def parse_resume(self, uploaded_file):
        prompt = """
        Parse this resume.

        Return ONLY JSON.

        {
            "personal_information": {},
            "summary": "",
            "skills": [],
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": []
        }
        """
        file_part = self._build_file_part(uploaded_file)
        response = self.client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=[file_part, prompt]
        )
        return self._clean_text(response.text)

    def parse_job(self, uploaded_file):
        prompt = """
        Parse this job description.

        Return JSON.

        {
            "title":"",
            "required_skills":[],
            "preferred_skills":[],
            "responsibilities":[],
            "experience":"",
            "education":""
        }
        """
        file_part = self._build_file_part(uploaded_file)
        response = self.client.models.generate_content(
            model='gemini-3.1-flash-lite',
            contents=[file_part, prompt]
        )
        return self._clean_text(response.text)
