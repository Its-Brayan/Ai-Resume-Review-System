from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import CAREER_ADVISOR_AGENT_PROMPT
from Code.prompt_builder import build_prompt_body

class CareerAdvisorAgent:
    llm = get_llm()

    def career_advice(self,query):
        config = load_config(CAREER_ADVISOR_AGENT_PROMPT)
        prompt = build_prompt_body(config['career_advisor_agent'],query)
        output = self.llm.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        result = {
            'career_advice':output
        }
        return result