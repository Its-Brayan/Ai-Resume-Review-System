import sys
import os
from typing import TypedDict
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT_DIR)
from Agents import(
    SupervisorAgent,
    SkillsGapAgent,
    ResumeParserAgent,
    ResumeImprovementAgent,
    JobAnalyzerAgent,
    AtsScoringAgent,
    CareerAdvisorAgent,
    ReportGeneratorAgent
)
from langgraph.graph import StateGraph,END
SupervisorAgent = SupervisorAgent.SupervisorAgent()
SkillsGapAgent = SkillsGapAgent.SkillsGapAgent()
ResumeParserAgent = ResumeParserAgent.ResumeParserAgent()
ResumeImprovementAgent = ResumeImprovementAgent.ResumeImprovementAgent()
JobAnalyzerAgent = JobAnalyzerAgent.JobAnalyzerAgent()
AtsScoringAgent = AtsScoringAgent.AtsScoringAgent()
CareerAdvisorAgent = CareerAdvisorAgent.CareerAdvisorAgent()
ReportGeneratorAgent = ReportGeneratorAgent.ReportGeneratorAgent()



class ResumeAgent(TypedDict):
    resume: str
    job_description: str
    execution_plan: list[str]
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

def supervisor_node(state:ResumeAgent):
    print("Supervisor agent is thinking...")
    plan = []
    if state['resume']:
        plan.extend(['resume_parser','ats_scorer'])

    if state['job_description']:
        plan.extend(['job_analyzer'])
    return{
        'execution_plan':plan
    }

def resumer_parser_node(state:ResumeAgent):
    print("Analyzing your resume")
    resume_parser = ResumeParserAgent.resume_parser(state['resume'])
    result = resume_parser['resume_parser_result']
    clean_text = unwrap_result(result)
    return{
        'resume_parser':clean_text
    }

def Job_analyzer_node(state:ResumeAgent):
    print("Analyzing the Job description")
    job_analyzer = JobAnalyzerAgent.job_analyzer(state['job_description'])
    result = job_analyzer['job_analyzer']
    clean_text = unwrap_result(result)
    return{
        'job_analyzer':clean_text
    }

def Ats_scorer_node(state:ResumeAgent):
    print("Giving your resume an ATS score...")
    ats_scorer = AtsScoringAgent.ats_scorer(state['resume'])
    result = ats_scorer['ats_score']
    clean_text = unwrap_result(result)
    return{
        'ats_scorer':clean_text
    }

def skills_gap_node(state:ResumeAgent):
    print("Analyzing your skills...")
    skills_analyzer = SkillsGapAgent.skills_agent([state['resume_parser'],state['ats_scorer'],state['job_analyzer']])
    result = skills_analyzer['skills_parser_result']
    clean_text = unwrap_result(result)
    return{
        'skills':clean_text
    }

def resume_improvement_node(state:ResumeAgent):
    print("Analyzing your resume for what to change...")
    combined_previous_output = {
    "parsed_resume": state["resume_parser"],
    "job_analysis": state["job_analyzer"],
    "skills_gap": state["skills"]
    }
    final_resume = ResumeImprovementAgent.resume_improver(combined_previous_output)
    result = final_resume['resume_improver']
    clean_text = unwrap_result(result)
    return{
        'resume_improver':clean_text
    }

def career_advice_node(state:ResumeAgent):
    print("Giving you the best career advice...")
    career_input = {
    "resume": state["resume_parser"],
    "skills": state["skills"],
    "improved_resume": state["resume_improver"]
}
    career_advisor = CareerAdvisorAgent.career_advice(career_input)
    result = career_advisor['career_advice']
    clean_text = unwrap_result(result)
    return{
        'career_advice':clean_text
    }

def final_report_node(state:ResumeAgent):
    print("Generating final report...")
    report = {
    "parsed_resume": state["resume_parser"],
    "ats": state["ats_scorer"],
    "job_analysis": state["job_analyzer"],
    "skills_gap": state["skills"],
    "resume_improvements": state["resume_improver"],
    "career_advice": state["career_advice"]
}
    final_report = ReportGeneratorAgent.generate_report(report)
    result = final_report['final_report']
    clean_text = unwrap_result(result)
    return{
        'final_report':clean_text
    }

def router_node(state:ResumeAgent):
    return state['execution_plan']
def run_graph() -> StateGraph:
    workflow = StateGraph(ResumeAgent)

    workflow.add_node('supervisor',supervisor_node)
    workflow.add_node('skills_checker',skills_gap_node)
    workflow.add_node('resume_parser',resumer_parser_node)
    workflow.add_node('resume_improver',resume_improvement_node)
    workflow.add_node('job_analyzer',Job_analyzer_node)
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
            'resume_parser':'resume_parser',
            'ats_scorer':'ats_scorer',
            'job_analyzer':'job_analyzer'
        }
    )
    workflow.add_edge('resume_parser','skills_checker')
    workflow.add_edge('ats_scorer','skills_checker')
    workflow.add_edge('job_analyzer','skills_checker')
    workflow.add_edge('skills_checker','resume_improver')
    workflow.add_edge('resume_improver','career_advisor')
    workflow.add_edge('career_advisor','final_report')
    workflow.add_edge('final_report',END)

    return workflow.compile()


def run_pipeline(resume,job_description):
     print(f"\n{'='*60}")
     print(f"Starting pipeline...")
     print(f"\n{'='*60}\n")

     graph = run_graph()
     result = graph.invoke(
         {
             'resume':resume,
              'job_description' :job_description,
              'execution_plan':[],
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


