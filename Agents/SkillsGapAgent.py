from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import SKILLS_GAP_AGENT_PROMPT
from Code.prompt_builder import build_prompt_body
from typing import List
class SkillsGapAgent:
    llm = get_llm('gemini-3.5-flash')

    def skills_agent(self,query:List[str]):
        config = load_config(SKILLS_GAP_AGENT_PROMPT)
        prompt = build_prompt_body(config['skills_matching_agent'],query)
        output = self.llm.invoke(prompt)
        result = {
            'skills_parser_result':output
        }
        return result