import sys
import os
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



class ResumeAgent:
    query: str
    supervise : str
    skills : str
    parser : str
    job_analyzer: str
    resume_improver: str
    final_report: str
    career_advice: str
    ats_scorer: str

def supervisor_node(state:ResumeAgent):
    print("Supervisor agent is thinking...")
    supervisor_plan = SupervisorAgent.plan(state['query'])
    result = supervisor_plan['supervisor_path']
    return{
        'supervise':result
    }

def resumer_parser_node(state:ResumeAgent):
    print("Analyzing your resume")
    resume_parser = ResumeParserAgent.resume_parser(state['query'])
    result = resume_parser['resume_parser_result']
    return{
        'parser':result
    }

def Job_analyzer_node(state:ResumeAgent):
    print("Analyzing the Job description")
    job_analyzer = JobAnalyzerAgent.job_analyzer(state['query'])
    result = job_analyzer['job_analyzer']
    return{
        'job_analyzer':result
    }

def Ats_scorer_node(state:ResumeAgent):
    print("Giving your resume an ATS score...")
    ats_scorer = AtsScoringAgent.ats_scorer(state['query'])
    result = ats_scorer['ats_score']
    return{
        'ats_scorer':result
    }

def skills_gap_node(state:ResumeAgent):
    print("Analyzing your skills...")
    skills_analyzer = SkillsGapAgent.skills_agent(state['query'])
    result = skills_analyzer['skills_parser_result']
    return{
        'skills':result
    }

def resume_improvement_node(state:ResumeAgent):
    print("Analyzing your resume for what to change...")
    final_resume = ResumeImprovementAgent.resume_improver(state['query'])
    result = final_resume['resume_improver']
    return{
        'resume_improver':result
    }

def career_advice_node(state:ResumeAgent):
    print("Giving you the best career advice...")
    career_advisor = CareerAdvisorAgent.career_advice(state['query'])
    result = career_advisor['career_advice']
    return{
        'career_advice':result
    }

def final_report_node(state:ResumeAgent):
    print("Generating final report...")
    final_report = ReportGeneratorAgent.generate_report(state['query'])
    result = final_report['final_report']
    return{
        'final_report':result
    }

def run_graph() -> StateGraph:
    workflow = StateGraph(ResumeAgent)

    workflow.add_node('supervisor',supervisor_node)
    workflow.add_node('skills_checker',skills_gap_node)
    workflow.add_node('resume_parser',resumer_parser_node)
    workflow.add_node('resume_improver',resume_improvement_node)
    workflow.add_node('job_analyzer',Job_analyzer_node)
    workflow.add_node('career_advisor',career_advice_node)
    workflow.add_node('ats_scorer',Ats_scorer_node)

    workflow.set_entry_point('supervisor')

    # workflow.add_edge('supervisor','resume_parser')
    # workflow.add_edge('supervisor','ats_scorer')
    # workflow.add_edge('supervisor','job_analyzer')
    workflow.add_conditional_edges(
        'supervisor',
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
    workflow.add_edge('career_advisor','final_improver')
    workflow.add_edge('final_improver',END)

    return workflow.compile()


def run_pipeline(query:str):
     print(f"\n{'='*60}")
     print(f"Starting pipeline for {query}")
     print(f"\n{'='*60}\n")

     graph = run_graph()
     result = graph.invoke(
         {
             'query':query,
              'supervise' :'',
              'skills' :'',
              'parser' : '',
              'job_analyzer': '',
              'resume_improver':'',
              'final_report':'',
              'career_advice': '',
              'ats_scorer': ''

         }
     )
     print(f"\n{'='*60}")
     print(f"Pipeline Complete")
     print(f"{'='*60}\n")

     return result


