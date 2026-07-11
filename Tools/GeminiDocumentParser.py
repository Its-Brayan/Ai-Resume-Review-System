from google import genai

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

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                uploaded_file,
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
     response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[
                uploaded_file,
                prompt
            ]
        )

     return response  