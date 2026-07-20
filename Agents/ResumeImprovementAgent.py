from Code.llm import get_groq_llm, get_gemini_llm
from Code.paths import RESUME_IMPROVEMENT_AGENT_PROMPT
from Code.load_yaml import load_config
from Code.prompt_builder import build_prompt_body

class ResumeImprovementAgent:
    llm = get_gemini_llm()

    def resume_improver(self,query:str):
        config = load_config(RESUME_IMPROVEMENT_AGENT_PROMPT)
        prompt = build_prompt_body(config['resume_improvement_agent'],query)
        output = self.llm.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt
        )
        result = {
            "resume_improver":output.text
        }
        return result