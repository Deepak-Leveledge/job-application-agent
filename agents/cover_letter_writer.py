from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from states.agent_state import AgentState
import os
from dotenv import load_dotenv
load_dotenv()


## Initialize the Gemeni API client
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))



@traceable(name="Cover Letter Writer Agent")
def cover_letter_writer_agent(state: AgentState) -> AgentState:
    print("✍️ Cover Letter Writer Agent running...")

    jd_analysis      = state["jd_analysis"]
    resume_analysis  = state["resume_analysis"]
    market_research  = state["market_research"]
    match_analysis   = state["match_analysis"]

    prompt = f"""
    You are an expert Cover Letter Writer with 10+ years
    of experience helping candidates land their dream jobs.

    Write a highly personalized and compelling cover letter
    using all the context provided below.

    STRICT RULES:
    - Do NOT write a generic cover letter
    - Mention the company name specifically
    - Reference something specific about the company
      from the market research (news, mission, values)
    - Highlight the candidate's TOP 3 strong matches
    - Address 1 skill gap positively
      (show willingness to learn)
    - Keep it to 4 paragraphs maximum
    - Keep tone professional yet personable
    - End with a strong confident closing
    - Do NOT use placeholder text like [Your Name]
      use actual details from resume analysis

    COVER LETTER STRUCTURE:
    Paragraph 1 — Strong opening, mention role and company,
                  show you know about the company
    Paragraph 2 — Your strongest relevant experience
                  and achievements
    Paragraph 3 — Why you are a great fit and address
                  one gap positively
    Paragraph 4 — Strong confident closing with call to action

    ---
    JD Analysis:
    {jd_analysis}

    ---
    Resume Analysis:
    {resume_analysis}

    ---
    Market Research:
    {market_research}

    ---
    Match Analysis:
    {match_analysis}
    """

    response = llm.invoke(prompt)

    # write output back to state
    state["cover_letter"] = response.content

    print("✅ Cover Letter Writer Agent done!")
    return state