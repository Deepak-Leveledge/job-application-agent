from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from states.agent_state import AgentState
import os
from dotenv import load_dotenv
load_dotenv()


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))


@traceable(name="Resume Analyzer Agent")
def resume_analyzer_agent(state: AgentState) -> AgentState:
    print("📄 Resume Analyzer Agent running...")

    resume = state["resume_text"]

    prompt = f"""
    You are an expert Resume Analyzer.
    Carefully analyze the following resume and extract:

    1. Candidate Name
    2. Current Job Title
    3. Total Years of Experience
    4. Technical Skills
    5. Soft Skills
    6. Work Experience (company, role, duration)
    7. Key Achievements
    8. Education
    9. Certifications (if any)
    10. Projects (if any)

    Be specific and structured in your response.
    Format each section clearly with headings.

    Resume:
    {resume}
    """

    response = llm.invoke(prompt)

    # write output back to state
    state["resume_analysis"] = response.content

    print("✅ Resume Analyzer Agent done!")
    return state