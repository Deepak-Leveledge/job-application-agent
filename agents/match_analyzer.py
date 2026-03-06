from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from states.agent_state import AgentState
import os
from dotenv import load_dotenv
load_dotenv()


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))



@traceable(name="Match Analyzer Agent")
def match_analyzer_agent(state: AgentState) -> AgentState:
    print("🔍 Match Analyzer Agent running...")

    jd_analysis = state["jd_analysis"]
    resume_analysis = state["resume_analysis"]
    market_research = state["market_research"]

    prompt = f"""
    You are an expert Career Coach and Job Match Analyzer.
    
    Carefully compare the Job Description Analysis with the 
    Candidate Resume Analysis and provide:

    1. MATCH SCORE
       - Give an overall match score from 0 to 100
       - Format exactly like this → Match Score: 75/100
       - Be honest and realistic

    2. STRONG MATCHES
       - List skills and experience the candidate HAS
         that the job WANTS
       - Be specific with examples from the resume

    3. SKILL GAPS
       - List skills and experience the job WANTS
         but the candidate DOES NOT have
       - Be honest and clear

    4. HIDDEN STRENGTHS
       - List candidate skills that are relevant to the role
         but not directly mentioned in the JD
       - These are bonus points for the candidate

    5. OVERALL ASSESSMENT
       - A short honest paragraph about the candidate's
         fit for this role
       - Should the candidate apply? Why?

    6. KEY ADVICE
       - Top 3 things the candidate should emphasize
         when applying for this role

    Use the market research context to make your analysis
    more relevant and accurate.

    ---
    JD Analysis:
    {jd_analysis}

    ---
    Resume Analysis:
    {resume_analysis}

    ---
    Market Research Context:
    {market_research}
    """

    response = llm.invoke(prompt)

    # write output back to state
    state["match_analysis"] = response.content

    print("✅ Match Analyzer Agent done!")
    return state

