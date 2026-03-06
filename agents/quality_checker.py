from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from states.agent_state import AgentState
import os
from dotenv import load_dotenv
load_dotenv()


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))




@traceable(name="Quality Checker Agent")
def quality_checker_agent(state: AgentState) -> AgentState:
    print("✅ Quality Checker Agent running...")

    cover_letter       = state["cover_letter"]
    resume_suggestions = state["resume_suggestions"]
    match_analysis     = state["match_analysis"]
    jd_analysis        = state["jd_analysis"]
    resume_analysis    = state["resume_analysis"]

    prompt = f"""
    You are a strict Quality Control Expert reviewing
    outputs from an AI Job Application Assistant.

    Review ALL the outputs below and check for quality.

    CHECK COVER LETTER FOR:
    - Is it personalized? (mentions company name?)
    - Is it relevant to the job?
    - Does it highlight strong matches?
    - Is it professional in tone?
    - Is it free of placeholder text like [Your Name]?
    - Is it 4 paragraphs or less?

    CHECK MATCH ANALYSIS FOR:
    - Is the match score realistic and justified?
    - Are skill gaps honestly identified?
    - Are strong matches actually relevant?

    CHECK RESUME SUGGESTIONS FOR:
    - Are suggestions specific not generic?
    - Do they reference actual resume content?
    - Are they actionable?

    RESPOND IN THIS EXACT FORMAT:

    COVER LETTER QUALITY: PASS or FAIL
    Reason: <one line reason>

    MATCH ANALYSIS QUALITY: PASS or FAIL
    Reason: <one line reason>

    RESUME SUGGESTIONS QUALITY: PASS or FAIL
    Reason: <one line reason>

    OVERALL: APPROVED or NEEDS REVISION
    Summary: <two line overall summary>

    ---
    JD Analysis:
    {jd_analysis}

    ---
    Resume Analysis:
    {resume_analysis}

    ---
    Match Analysis:
    {match_analysis}

    ---
    Cover Letter:
    {cover_letter}

    ---
    Resume Suggestions:
    {resume_suggestions}
    """

    response = llm.invoke(prompt)
    result = response.content.strip()

    print(f"\n📋 Quality Report:\n{result}")

    # parse if overall approved or not
    if "OVERALL: APPROVED" in result:
        state["quality_approved"] = True
        print("✅ Quality Check PASSED!")
    else:
        state["quality_approved"] = False
        print("⚠️ Quality Check FAILED — needs revision!")

    # store the quality report in final output
    state["final_output"] = result

    return state

