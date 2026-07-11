from Code.llm import get_llm
from Code.load_yaml import load_config
from Code.paths import RESUME_PARSER_AGENT_PROMPT
from Code.prompt_builder import build_prompt_body
from google.genai import types
class ResumeParserAgent:
    client = get_llm()
    def resume_parser(self,resume_text):
        resume_text.seek(0)
        file_part = types.Part.from_bytes(
            data=resume_text.read(),
            mime_type=resume_text.type
        )
        config = load_config(RESUME_PARSER_AGENT_PROMPT)
        prompt = build_prompt_body(config['resume_parser_agent'],file_part)
        output = self.client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt)
        result = {
            "resume_parser_result":output
        }
        return result