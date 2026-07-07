from Code.llm import get_llm
from Code.prompt_builder import build_prompt_body
from Code.paths import REPORT_GENERATOR_AGENT_PROMPT
from Code.load_yaml import load_config

class ReportGeneratorAgent:
    llm = get_llm('llama-3.3-70b-versatile')

    def generate_report(self,query:str):
        config = load_config(REPORT_GENERATOR_AGENT_PROMPT)
        prompt = build_prompt_body(config,query)
        output = self.llm.invoke(prompt)
        result = {
            'final_report':output
        }
        return result