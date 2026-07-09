from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import RESUME_PARSER_AGENT_PROMPT
from Code.prompt_builder import build_prompt_body
class ResumeParserAgent:
    llm = get_llm("gemini-3.5-flash")

    def resume_parser(self,resume_text:str):
        config = load_config(RESUME_PARSER_AGENT_PROMPT)
        prompt = build_prompt_body(config['resume_parser_agent'],resume_text)
        output = self.llm.invoke(prompt)
        result = {
            "resume_parser_result":output
        }
        return result