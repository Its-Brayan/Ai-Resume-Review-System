from Code.llm import get_llm
from Code.paths import JOB_ANALYZER_AGENT_PROMPT
from Code.prompt_builder import build_prompt_body
from Code.load_yaml import load_config


class JobAnalyzerAgent:
    llm = get_llm('llama-3.3-70b-versatile')

    def job_analyzer(self,job_description:str):
        config = load_config(JOB_ANALYZER_AGENT_PROMPT)
        prompt = build_prompt_body(config,job_description)
        output = self.llm.invoke(prompt)
        result = {
            'job_analyzer':output
        }
        return result