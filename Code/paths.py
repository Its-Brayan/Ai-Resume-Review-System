import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(ROOT_DIR,'Config')
ATS_AGENT_PROMPT = os.path.join(CONFIG_DIR,'Ats_agent_prompt.yaml')
CAREER_ADVISOR_AGENT_PROMPT = os.path.join(CONFIG_DIR,'career_advisor_agent_prompt.yaml')
JOB_ANALYZER_AGENT_PROMPT = os.path.join(CONFIG_DIR,'job_analyzer_prompt.yaml')
RESUME_IMPROVEMENT_AGENT_PROMPT = os.path.join(CONFIG_DIR,'resume_improver_agent_prompt.yaml')
RESUME_PARSER_AGENT_PROMPT = os.path.join(CONFIG_DIR,'resume_parser_agent_prompt.yaml')
SKILLS_GAP_AGENT_PROMPT = os.path.join(CONFIG_DIR,'skills_gap_agent_prompt.yaml')
SUPERVISOR_AGENT_PROMPT = os.path.join(CONFIG_DIR,'supervisor_agent_prompt.yaml')
REPORT_GENERATOR_AGENT_PROMPT = os.path.join(CONFIG_DIR,'report_generator_prompt.yaml')