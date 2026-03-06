from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from states.agent_state import AgentState
import os
from tools.search_tool import search_web
from dotenv import load_dotenv
load_dotenv()


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))




@traceable(name="Market Researcher Agent")
def market_researcher_agent(state: AgentState) -> AgentState:
    print("🌐 Market Researcher Agent running...")

    jd_analysis = state["jd_analysis"]

    # step 1 — extract company name and role from jd analysis
    extract_prompt = f"""
    From the following job description analysis, extract:
    1. Company Name
    2. Job Title / Role

    Return ONLY in this exact format:
    Company: <company name>
    Role: <job title>

    If company name is not found, write: Company: Unknown

    JD Analysis:
    {jd_analysis}
    """

    extract_response = llm.invoke(extract_prompt)
    extracted = extract_response.content.strip()

    print(f"📌 Extracted info: {extracted}")

    # parse company and role
    company = "Unknown"
    role = "Unknown"

    for line in extracted.split("\n"):
        if line.startswith("Company:"):
            company = line.replace("Company:", "").strip()
        if line.startswith("Role:"):
            role = line.replace("Role:", "").strip()

    # step 2 — search the web
    search_results = ""

    if company != "Unknown":
        # search company info
        search_results += search_web(f"{company} company overview mission values culture")
        # search recent news
        search_results += search_web(f"{company} latest news 2024 2025")
    
    # search role in market
    search_results += search_web(f"{role} skills requirements job market 2026 to 2030")

    # step 3 — summarize findings with gemini
    summarize_prompt = f"""
    You are a Market Research Expert.
    Based on the following web search results, provide a concise summary of:

    1. Company Overview (what they do, their mission)
    2. Company Culture and Values
    3. Recent News about the company
    4. Market demand for the role: {role}
    5. Key things this company looks for in candidates
    6. Any important insights for a job applicant

    Search Results:
    {search_results}
    """

    summary_response = llm.invoke(summarize_prompt)

    # write output back to state
    state["market_research"] = summary_response.content

    print("✅ Market Researcher Agent done!")
    return state