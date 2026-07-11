from Code.paths import SUPERVISOR_AGENT_PROMPT
from Code.load_yaml import load_config
from Code.llm import get_groq_llm
from Code.prompt_builder import build_prompt_body

class SupervisorAgent:
    llm = get_groq_llm('llama-3.3-70b-versatile')
     
    def plan(self,query:list):
       config = load_config(SUPERVISOR_AGENT_PROMPT)
       prompt = build_prompt_body(config['supervisor_agent'],query)
       print(f"Here is the prompt: {prompt}")
       output = self.llm.invoke(prompt)

       result = {
         'supervisor_path':output
       }
       return result