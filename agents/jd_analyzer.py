from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from states.agent_state import AgentState
import os
from dotenv import load_dotenv
load_dotenv()


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))


@traceable(name="JD Analyzer Agent")
def jd_analyzer_agent(state: AgentState) -> AgentState:
    print("🔍 JD Analyzer Agent running...")

    jd = state["job_description"]

    prompt = f"""
    You are an expert Job Description Analyzer.
    Carefully analyze the following job description and extract:

    1. Job Title
    2. Company Name (if mentioned)
    3. Required Technical Skills
    4. Required Soft Skills
    5. Years of Experience Required
    6. Key Responsibilities
    7. Must Have Qualifications
    8. Nice to Have Qualifications
    9. Company Culture Keywords
    10. Any other important information

    Be specific and structured in your response.
    Format each section clearly with headings.

    Job Description:
    {jd}
    """


    response = llm.invoke(prompt)

    # write output back to state
    state["jd_analysis"] = response.content

    print("✅ JD Analyzer Agent done!")
    return state

