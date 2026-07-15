from google import genai
from google.genai import types
class GeminiDocumentParser:
    def __init__(self):
        self.client = genai.Client()
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
        file_part = types.Part.from_bytes(
            data=uploaded_file.read(),
            mime_type=uploaded_file.type
        )
        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                file_part,
                prompt
            ]
        )

        return response.text
    
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
     file_part = types.Part.from_bytes(
            data=uploaded_file.read(),
            mime_type=uploaded_file.type
        )
   
     response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                file_part,
                prompt
            ]
        )

     return response  