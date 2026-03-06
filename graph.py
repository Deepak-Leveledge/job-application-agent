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
from langgraph.graph import StateGraph, END

import os

load_dotenv()


def should_revise(state: AgentState) -> str:
    """
    Conditional edge — checks if quality approved.
    If not approved → go back to cover letter writer.
    If approved → end the graph.
    """
    if state["quality_approved"]:
        print("✅ Quality approved — finishing!")
        return "approved"
    else:
        print("⚠️ Quality failed — revising cover letter...")
        return "revise"


def build_graph():
    # initialize graph with our state
    graph = StateGraph(AgentState)

    # add all agent nodes
    graph.add_node("jd_analyzer",          jd_analyzer_agent)
    graph.add_node("resume_analyzer",      resume_analyzer_agent)
    graph.add_node("market_researcher",    market_researcher_agent)
    graph.add_node("match_analyzer",       match_analyzer_agent)
    graph.add_node("cover_letter_writer",  cover_letter_writer_agent)
    graph.add_node("resume_improver",      resume_improver_agent)
    graph.add_node("quality_checker",      quality_checker_agent)

    # set entry point
    graph.set_entry_point("jd_analyzer")

    # add edges between nodes
    graph.add_edge("jd_analyzer",         "resume_analyzer")
    graph.add_edge("resume_analyzer",     "market_researcher")
    graph.add_edge("market_researcher",   "match_analyzer")
    graph.add_edge("match_analyzer",      "cover_letter_writer")
    graph.add_edge("cover_letter_writer", "resume_improver")
    graph.add_edge("resume_improver",     "quality_checker")

    # conditional edge after quality checker
    # if approved → END
    # if not approved → revise cover letter
    graph.add_conditional_edges(
        "quality_checker",
        should_revise,
        {
            "approved": END,
            "revise":   "cover_letter_writer"
        }
    )

    # compile and return graph
    return graph.compile()

