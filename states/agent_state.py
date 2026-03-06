from typing import Any, Dict,Optional,List,TypedDict

class AgentState(TypedDict):

    #User input 
    job_description: str        # raw job description pasted by user
    resume_text: str            # raw resume text extracted from PDF

    #Agent Output
    jd_analysis: Optional[str]          # output from JD Analyzer Agent
    resume_analysis: Optional[str]      # output from Resume Analyzer Agent
    market_research: Optional[str]      # output from Market Researcher Agent
    match_analysis: Optional[str]       # output from Match Analyzer Agent
    cover_letter: Optional[str]         # output from Cover Letter Writer Agent
    resume_suggestions: Optional[str]   # output from Resume Improver Agent
    quality_approved: Optional[bool]    # output from Quality Checker Agent
    final_output: Optional[str]         # final combined output for user


    #error output
    error: Optional[str]                # error message if any agent fails