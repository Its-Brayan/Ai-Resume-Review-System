from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import ATS_AGENT_PROMPT
from Code.prompt_builder import build_prompt_body

class AtsScoringAgent:
    llm = get_llm('llama-3.3-70b-versatile')

    def ats_scorer(self,resume_text:str):
        config = load_config(ATS_AGENT_PROMPT)
        prompt = build_prompt_body(config['ats_review_agent'],resume_text)
        output = self.llm.invoke(prompt)
        result = {
            'ats_score':output
        }
        return result