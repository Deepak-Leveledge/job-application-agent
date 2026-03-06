from dotenv import load_dotenv
from states.agent_state import AgentState 
from agents.jd_analyzer import jd_analyzer_agent
from tools.pdf_reader import read_pdf
from agents.resume_analyzer import resume_analyzer_agent
from agents.market_researcher import market_researcher_agent
from agents.match_analyzer import match_analyzer_agent
from agents.cover_letter_writer import cover_letter_writer_agent
from agents.resume_improver import resume_improver_agent
from agents.quality_checker import quality_checker_agent  
from graph import build_graph  
import os

load_dotenv()

# Test all keys  Testing for steup is done or not 
# print("Gemini Key:", os.getenv("GEMINI_API_KEY")[:5], "...")
# print("Tavily Key:", os.getenv("TAVILY_API_KEY")[:5], "...")
# print("LangSmith Key:", os.getenv("LANGSMITH_API_KEY")[:5], "...")
# print("LangSmith Project:", os.getenv("LANGSMITH_PROJECT"))
# print("LangSmith Tracing:", os.getenv("LANGSMITH_TRACING"))
# print("✅ Setup is working!")


# create a test state
# test_state: AgentState = {
#     "job_description": "We are looking for a Python Developer...",
#     "resume_text": "I am a Python developer with 2 years of experience...",
#     "jd_analysis": None,
#     "resume_analysis": None,
#     "market_research": None,
#     "match_analysis": None,
#     "cover_letter": None,
#     "resume_suggestions": None,
#     "quality_approved": None,
#     "final_output": None,
#     "error": None,
# }

# print("✅ State created successfully!")
# print("Job Description:", test_state["job_description"][:30], "...")
# print("Resume Text:", test_state["resume_text"][:30], "...")
# print("All other fields are None — ready for agents to fill!")



# read resume from PDF
resume_text = read_pdf("C:\\Users\\DELL\\OneDrive\\Desktop\\job-application-agent\\Deepak_Gupta_AIML_Developer_Resume.pdf")

sample_jd = """
Our vision for the future is based on the idea that transforming financial lives starts by giving our people the freedom to transform their own. We have a flexible work environment, and fluid career paths. We not only encourage but celebrate internal mobility. We also recognize the importance of purpose, well-being, and work-life balance. Within Empower and our communities, we work hard to create a welcoming and inclusive environment, and our associates dedicate thousands of hours to volunteering for causes that matter most to them.

Chart your own path and grow your career while helping more customers achieve financial freedom. Empower Yourself.

The AI/ML Engineer is responsible for designing, building, and optimizing AI and machine learning solutions within the Generative AI Platform. This role involves coding in Python and using relevant AI frameworks to develop scalable models and data pipelines. By collaborating with cross-functional teams, the AI/ML Engineer ensures that the platform’s AI capabilities meet technical and business objectives.

ESSENTIAL FUNCTIONS

Model Development & Deployment

Build and deploy machine learning models using Python and relevant libraries (e.g., TensorFlow, PyTorch, scikit-learn).
Optimize models for performance, scalability, and security.

Data Pipeline Management

Collaborate with data engineers to design robust data pipelines for model training and inference.
Validate and preprocess datasets to ensure model accuracy and reliability.

Research & Innovation

Stay current on the latest AI/ML trends and incorporate best practices into the platform.
Experiment with novel techniques in generative AI and provide recommendations for platform enhancements.

QUALIFICATIONS

Bachelor’s degree in Computer Science, Data Science, or related field; Master’s preferred.
3+ years of AI/ML development experience.
Strong Python programming skills and familiarity with major AI/ML frameworks.
Experience deploying models into production environments (cloud or on-prem).
AI/ML certifications from AWS, Azure, or Google Cloud are beneficial.
Strong analytical thinking and problem-solving.
Detail-oriented with an emphasis on model reliability and validation.
Excellent communication skills for cross-functional collaboration.
Occasional need to support after-hours release cycles or troubleshooting.
Authority to recommend new AI/ML tools and frameworks for adoption.
Collaborates with product managers, data engineers, and QA teams.
May interface with external vendors for AI tools.
Normal Office Working Conditions: Office based with potential for remote or hybrid.

We are an equal opportunity employer with a commitment to diversity. All individuals, regardless of personal characteristics, are encouraged to apply. All qualified applicants will receive consideration for employment without regard to age, race, color, national origin, ancestry, sex, sexual orientation, gender, gender identity, gender expression, marital status, pregnancy, religion, physical or mental disability, military or veteran status, genetic information, or any other status protected by applicable state or local law. 
"""

# create initial state
state: AgentState = {
    "job_description": sample_jd,
    "resume_text": resume_text,
    "jd_analysis": None,
    "resume_analysis": None,
    "market_research": None,
    "match_analysis": None,
    "cover_letter": None,
    "resume_suggestions": None,
    "quality_approved": None,
    "final_output": None,
    "error": None,
}

# # run agent 1
# state = jd_analyzer_agent(state)

# # run agent 2
# state = resume_analyzer_agent(state)

# # run agent 3
# state = market_researcher_agent(state)

# # run agent 4
# state = match_analyzer_agent(state)

# # run agent 5
# state = cover_letter_writer_agent(state)

# # run agent 6
# state = resume_improver_agent(state)

# # run agent 7
# state = quality_checker_agent(state)


# build and run the graph
print("🚀 Starting Job Application Agent...\n")
graph = build_graph()
final_state = graph.invoke(state)


# print results
# print("\n========== JD ANALYSIS ==========")
# print(state["jd_analysis"])

# print("\n========== RESUME ANALYSIS ==========")
# print(state["resume_analysis"])


# print("\n========== MARKET RESEARCH ==========")
# print(state["market_research"])



# print("\n========== MATCH ANALYSIS ==========")
# print(state["match_analysis"])


# print("\n========== COVER LETTER ==========")
# print(state["cover_letter"])

# print("\n========== RESUME SUGGESTIONS ==========")
# print(state["resume_suggestions"])


# print("\n========== QUALITY CHECK ==========")
# print("Quality Approved:", state["quality_approved"])



# print final results
print("\n========== MATCH ANALYSIS ==========")
print(final_state["match_analysis"])

print("\n========== COVER LETTER ==========")
print(final_state["cover_letter"])

print("\n========== RESUME SUGGESTIONS ==========")
print(final_state["resume_suggestions"])

print("\n========== QUALITY REPORT ==========")
print(final_state["final_output"])

print("\n========== STATUS ==========")
print("✅ APPROVED!" if final_state["quality_approved"] else "⚠️ NEEDS REVISION!")


