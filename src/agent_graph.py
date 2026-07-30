from agent_state import AgentState
from langgraph.graph import StateGraph, END
from vision_tool_refactored import generate_caption
from vision_analysis_tool import analyse_image
from decision_tool import should_search
from search_tool import search_web

# ---------- Node 1: Vision Tool ----------
def caption_node(state: AgentState) -> AgentState:
    caption = generate_caption(state["image_path"])
    return {**state, "caption": caption}

# ---------- Node 2: Ollama Visiona anlaysis (detailed, location-aware)---------
def vision_analysis_node(state: AgentState) -> AgentState:
    analysis = analyse_image(state["image_path"])
    return {**state, "vision_analysis": analysis}

# ---------- Node 3: Decision-making ----------
def decision_node(state: AgentState) -> AgentState:
    decision = should_search(state["vision_analysis"])
    return {**state, "decision": decision}


# ---------- Node 3a: Web Search (only reached if SEARCH) ----------
def search_node(state: AgentState) -> AgentState:
    results = search_web(state["vision_analysis"])
    return {**state, "search_results": results}


# ---------- Node 3b / 4: Compile final report ----------
def report_node(state: AgentState) -> AgentState:
    report = f"## Caption\n{state['caption']}\n\n"
    report += f"## Detailed Analysis\n{state['vision_analysis']}\n\n"
 
    if state.get("search_results"):
        report += "## Additional Context\n"
        for r in state["search_results"]:
            report += f"- **{r['title']}**: {r['content'][:200]}...\n  Source: {r['url']}\n"
    else:
        report += "## Additional Context\nNo additional research was needed for this image."
 
    return {**state, "final_report": report}
 


# ---------- Conditional edge logic ----------
def route_decision(state: AgentState) -> str:
    if "SEARCH" in state["decision"]:
        return "search"
    return "skip"


# ---------- Build the graph ----------
graph = StateGraph(AgentState)

graph.add_node("caption", caption_node)
graph.add_node("vision_analysis", vision_analysis_node)
graph.add_node("decide", decision_node)
graph.add_node("search", search_node)
graph.add_node("report", report_node)

graph.set_entry_point("caption")
graph.add_edge("caption", "vision_analysis")
graph.add_edge("vision_analysis", "decide")

graph.add_conditional_edges(
    "decide",
    route_decision,
    {
        "search": "search",
        "skip": "report",
    },
)

graph.add_edge("search", "report")
graph.add_edge("report", END)

agent = graph.compile()


if __name__ == "__main__":
    result = agent.invoke({"image_path": "../landscape.jpg"})
    print(result["final_report"])
