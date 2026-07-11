from Code.llm import get_llm
from Code.paths import JOB_ANALYZER_AGENT_PROMPT
from Code.prompt_builder import build_prompt_body
from Code.load_yaml import load_config
from google.genai import types

class JobAnalyzerAgent:
    client = get_llm()

    def job_analyzer(self,job_description):
        job_description.seek(0)
        file_part = types.Part.from_bytes(
            data = job_description.read(),
            mime_type=job_description.type    
        )
        config = load_config(JOB_ANALYZER_AGENT_PROMPT)
        prompt = build_prompt_body(config['job_analysis_agent'],file_part)
        output = self.client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        result = {
            'job_analyzer':output
        }
        return result