import sys
import os
from typing import TypedDict, Any
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT_DIR)
from Agents import(
    SupervisorAgent,
    SkillsGapAgent,
    # ResumeParserAgent,
    ResumeImprovementAgent,
    # JobAnalyzerAgent,
    AtsScoringAgent,
    CareerAdvisorAgent,
    ReportGeneratorAgent
)
import json
from langgraph.graph import StateGraph,END
SupervisorAgent = SupervisorAgent.SupervisorAgent()
SkillsGapAgent = SkillsGapAgent.SkillsGapAgent()
# ResumeParserAgent = ResumeParserAgent.ResumeParserAgent()
ResumeImprovementAgent = ResumeImprovementAgent.ResumeImprovementAgent()
# JobAnalyzerAgent = JobAnalyzerAgent.JobAnalyzerAgent()
AtsScoringAgent = AtsScoringAgent.AtsScoringAgent()
CareerAdvisorAgent = CareerAdvisorAgent.CareerAdvisorAgent()
ReportGeneratorAgent = ReportGeneratorAgent.ReportGeneratorAgent()



class ResumeAgent(TypedDict):
    # resume: Any
    # job_description: Any
    resume:dict
    job:dict
    execution_plan: list[str]
    selected_tasks:list[str]
    skills : dict
    resume_parser : dict
    job_analyzer: dict
    resume_improver: dict
    final_report: dict
    career_advice: dict
    ats_scorer: dict

def unwrap_result(result):
    if hasattr(result, 'content'):
        result = result.content
    elif isinstance(result, dict):
        for key in ('content', 'text', 'output', 'response', 'message'):
            if key in result:
                result = result[key]
                break
    if isinstance(result, dict):
        return "\n".join(f"{k}: {unwrap_result(v)}" for k, v in result.items())
    if isinstance(result, list):
        return "\n".join(unwrap_result(item) for item in result)
    return str(result)


def parse_json_output(raw_result: Any):
    if isinstance(raw_result, (dict, list)):
        return raw_result
    if hasattr(raw_result, 'content'):
        raw_result = raw_result.content
    if isinstance(raw_result, dict):
        for key in ('content', 'text', 'output', 'response', 'message'):
            if key in raw_result:
                raw_result = raw_result[key]
                break
    if not isinstance(raw_result, str):
        raw_result = str(raw_result)

    text = raw_result.strip()
    text = text.replace('```json', '').replace('```', '').strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        lines = [line.strip('- ').strip() for line in text.splitlines() if line.strip()]
        return lines or [text]


def supervisor_node(state:ResumeAgent):
    print("Supervisor agent is thinking...")
    if state['execution_plan']:
        return{}
    supervisor = SupervisorAgent.plan({
       "resume":state['resume'], 
       "job":state['job'],
       "selected_tasks":state['selected_tasks']})
    result = supervisor['supervisor_path']
    plan = parse_json_output(result)

    if isinstance(plan, dict) and 'execution_plan' in plan:
        plan = plan['execution_plan']
    if isinstance(plan, str):
        plan = [plan]
    if not isinstance(plan, list):
        plan = [str(plan)]

    return {
        'execution_plan': plan
    }

# def resumer_parser_node(state:ResumeAgent):
#     print("Analyzing your resume")
#     resume_parser = ResumeParserAgent.resume_parser(state['resume'])
#     result = resume_parser['resume_parser_result']
#     clean_text = unwrap_result(result)
#     return{
#         'resume_parser':clean_text
#     }

# def Job_analyzer_node(state:ResumeAgent):
#     print("Analyzing the Job description")
#     job_analyzer = JobAnalyzerAgent.job_analyzer(state['job_description'])
#     result = job_analyzer['job_analyzer']
#     clean_text = unwrap_result(result)
#     return{
#         'job_analyzer':clean_text
#     }

def Ats_scorer_node(state:ResumeAgent):
    print("Giving your resume an ATS score...")
    ats_scorer = AtsScoringAgent.ats_scorer(state['resume'])
    result = ats_scorer['ats_score']
    remainder = state['execution_plan'][1:]
    clean_text = unwrap_result(result)
    return{
        'ats_scorer':clean_text,
        'execution_plan':remainder
    }

def skills_gap_node(state:ResumeAgent):
    print("Analyzing your skills...")
    skills_analyzer = SkillsGapAgent.skills_agent({
        "resume":state['resume'],
        "job":state['job']})
    result = skills_analyzer['skills_parser_result']
    remainder = state['execution_plan'][1:]
    clean_text = unwrap_result(result)
    return{
        'skills':clean_text,
        'execution_plan':remainder
    }

def resume_improvement_node(state:ResumeAgent):
    print("Analyzing your resume for what to change...")
    combined_previous_output = {
    # "original_resume":state['resume'],
    "parsed_resume": state["resume"],
    "skills_gap": state["skills"],
    "ats_score":state['ats_scorer']
    }
    final_resume = ResumeImprovementAgent.resume_improver(combined_previous_output)
    result = final_resume['resume_improver']
    remainder = state['execution_plan'][1:]
    clean_text = unwrap_result(result)
    return{
        'resume_improver':clean_text,
        'execution_plan':remainder
    }

def career_advice_node(state:ResumeAgent):
    print("Giving you the best career advice...")
    career_input = {
    "resume": state["resume"],
    "job":state['job'],
    "skills": state["skills"],
}
    career_advisor = CareerAdvisorAgent.career_advice(career_input)
    result = career_advisor['career_advice']
    remainder = state['execution_plan'][1:]
    clean_text = unwrap_result(result)
    return{
        'career_advice':clean_text,
        'execution_plan':remainder
    }

def final_report_node(state:ResumeAgent):
    print("Generating final report...")
    report = {
    "resume": state["resume"],
    "ats": state["ats_scorer"],
    "job": state["job"],
    "skills_gap": state["skills"],
    "resume_improvements": state["resume_improver"],
    "career_advice": state["career_advice"]
}
    final_report = ReportGeneratorAgent.generate_report(report)
    result = final_report['final_report']
    remainder = state['execution_plan'][1:]
    clean_text = unwrap_result(result)
    return{
        'final_report':clean_text,
        'execution_plan':remainder
    }

def router_node(state:ResumeAgent):
    plan = state['execution_plan']
    if not plan:
     return END

    route_map = {
        'ats_review': 'ats_scorer',
        'ats_scorer': 'ats_scorer',
        'skills_gap': 'skills_checker',
        'resume_improver': 'resume_improver',
        'career_advisor': 'career_advisor',
        'report_generator': 'final_report',
        'final_report': 'final_report'
    }

    next_step = str(plan[0]).strip().lower()
    mapped_step = route_map.get(next_step)
    if not mapped_step:
        print(f"Warning: unknown execution plan step '{plan[0]}', routing to final_report")
        mapped_step = 'final_report'

    return mapped_step


def run_graph() -> StateGraph:
    workflow = StateGraph(ResumeAgent)

    workflow.add_node('supervisor',supervisor_node)
    workflow.add_node('skills_checker',skills_gap_node)
    # workflow.add_node('resume_parser',resumer_parser_node)
    workflow.add_node('resume_improver',resume_improvement_node)
    # workflow.add_node('job_analyzer',Job_analyzer_node)
    workflow.add_node('career_advisor',career_advice_node)
    workflow.add_node('ats_scorer',Ats_scorer_node)
    workflow.add_node('final_report',final_report_node)

    workflow.set_entry_point('supervisor')

    # workflow.add_edge('supervisor','resume_parser')
    # workflow.add_edge('supervisor','ats_scorer')
    # workflow.add_edge('supervisor','job_analyzer')
    workflow.add_conditional_edges(
        'supervisor',
        router_node,
        {
       "ats_scorer": "ats_scorer",
        "skills_checker": "skills_checker",
        "resume_improver": "resume_improver",
        "career_advisor": "career_advisor",
        "final_report": "final_report",
        END : END
        }
    )
    # workflow.add_edge('resume_parser','supervisor')
    # workflow.add_edge('job_analyzer','supervisor')

    workflow.add_edge('ats_scorer','supervisor')
    # workflow.add_edge('job_analyzer','skills_checker')
    workflow.add_edge('skills_checker','supervisor')
    workflow.add_edge('resume_improver','supervisor')
    workflow.add_edge('career_advisor','supervisor')
    workflow.add_edge('final_report',END)

    return workflow.compile()

graph = run_graph()
def run_pipeline(resume,job_description,selected_tasks):
     print(f"\n{'='*60}")
     print(f"Starting pipeline...")
     print(f"\n{'='*60}\n")

    
     result = graph.invoke(
         {
             'resume':resume,
              'job':job_description,
              'execution_plan':[],
              'selected_tasks':selected_tasks,
              'skills' :{},
              'resume_parser' : {},
              'job_analyzer': {},
              'resume_improver':{},
              'final_report':{},
              'career_advice': {},
              'ats_scorer': {}

         }
     )
     print(f"\n{'='*60}")
     print(f"Pipeline Complete")
     print(f"{'='*60}\n")

     return result


