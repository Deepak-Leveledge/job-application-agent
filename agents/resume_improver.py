from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from states.agent_state import AgentState
import os
from dotenv import load_dotenv
load_dotenv()


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))




@traceable(name="Resume Improver Agent")
def resume_improver_agent(state: AgentState) -> AgentState:
    print("📝 Resume Improver Agent running...")

    jd_analysis     = state["jd_analysis"]
    resume_analysis = state["resume_analysis"]
    match_analysis  = state["match_analysis"]

    prompt = f"""
    You are an expert Resume Coach with deep knowledge of
    ATS (Applicant Tracking Systems) and hiring processes.

    Based on the job description analysis, resume analysis,
    and match analysis provided, give SPECIFIC and ACTIONABLE
    resume improvement suggestions.

    STRICT RULES:
    - Be very specific, not generic
    - Reference actual content from the resume
    - Reference actual requirements from the JD
    - Every suggestion must have a clear reason WHY
    - Prioritize suggestions by importance

    PROVIDE THE FOLLOWING SECTIONS:

    1. KEYWORDS TO ADD
       - List exact keywords from JD missing in resume
       - For each keyword suggest WHERE to add it
         in the resume naturally

    2. EXPERIENCE SECTION IMPROVEMENTS
       - Which bullet points to reword
       - Show before and after example for top 2

    3. SKILLS SECTION IMPROVEMENTS
       - What to add, remove or reorganize
       - How to group skills better

    4. ACHIEVEMENTS TO HIGHLIGHT
       - Which existing achievements are most relevant
       - How to quantify them better if possible

    5. WHAT TO REMOVE
       - Anything in the resume that is irrelevant
         to this specific role and wastes space

    6. ATS OPTIMIZATION TIPS
       - Specific tips to pass ATS for this job

    ---
    JD Analysis:
    {jd_analysis}

    ---
    Resume Analysis:
    {resume_analysis}

    ---
    Match Analysis:
    {match_analysis}
    """

    response = llm.invoke(prompt)

    # write output back to state
    state["resume_suggestions"] = response.content

    print("✅ Resume Improver Agent done!")
    return state

