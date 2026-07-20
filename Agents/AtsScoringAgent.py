from Code.llm import get_groq_llm
from Code.llm import get_gemini_llm
from Code.load_yaml import load_config
from Code.paths import ATS_AGENT_PROMPT
from Code.prompt_builder import build_prompt_body
from google.genai import types


class AtsScoringAgent:
    llm = get_gemini_llm()
    def ats_scorer(self,resume):
        # resume.seek(0)
        # file_part = types.Part.from_bytes(
        #     data=resume.read(),
        #     mime_type=resume.type
        # )
        config = load_config(ATS_AGENT_PROMPT)
        prompt = build_prompt_body(config['ats_review_agent'],resume)
        output = self.llm.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        result = {
            'ats_score':output
        }
        return result.text