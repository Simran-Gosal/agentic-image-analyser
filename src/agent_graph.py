'''
agent_graph.py

- the core of the project - the LangGraph orchestration that wires every individual tool into one runnable agent
- vision captioning, Ollama vision analysis, decision-making, web search
'''

#IMPORTS
from agent_state import AgentState
from langgraph.graph import StateGraph, END
from vision_tool_refactored import generate_caption, clean_caption_grammar
from vision_analysis_tool import analyse_image
from decision_tool import should_search
from search_tool import search_web

# ----- Node 1: Vision Tool -----

# generates a short, quick BLIP-large caption of the image
# runs first, since its fast and gives a baselines description before more detailed vision analysis step runs

def caption_node(state: AgentState) -> AgentState:
    raw_caption = generate_caption(state["image_path"])
    caption = clean_caption_grammar(raw_caption)
    return {**state, "caption": caption}

# ----- Node 2: Ollama Visiona anlaysis (detailed, location-aware) -----

# sends raw image directly to vision-capable Ollama model (llava)
# attempts identifying a specific location if one is recognisable 

def vision_analysis_node(state: AgentState) -> AgentState:
    analysis = analyse_image(state["image_path"])
    return {**state, "vision_analysis": analysis}

# ----- Node 3: Decision-making -----

#asks an LLM whether vision analysis contains anything specific enough to be worth researching further on the web

def decision_node(state: AgentState) -> AgentState:
    decision = should_search(state["vision_analysis"])
    return {**state, "decision": decision}


# ----- Node 3a: Web Search (only reached if SEARCH) -----

# runs an actual Tavily web search using the vision analysis text as the query
# so the final report can include real, external context

def search_node(state: AgentState) -> AgentState:
    combined_query = f"{state['caption']} {state['vision_analysis']}"
    results = search_web(combined_query)
    return {**state, "search_results": results}


# ----- Node 4: Compile final report -----
def report_node(state: AgentState) -> AgentState:
    #build final, human readable report by combining the caption, detailed vision analysis and the web search results
    report = f"## Caption\n{state['caption']}\n\n"
    report += f"## Detailed Analysis\n{state['vision_analysis']}\n\n"

    #context section has real content or a fallback message
    if state.get("search_results"):
        report += "## Additional Context\n"
        for r in state["search_results"]:
            report += f"- **{r['title']}**: {r['content'][:200]}...\n  Source: {r['url']}\n"
    else:
        report += "## Additional Context\nNo additional research was needed for this image."
 
    return {**state, "final_report": report}
 


# ----- Conditional edge logic -----

# reads decision made in decision_node and tells the graph which names branch to follow next

def route_decision(state: AgentState) -> str:
    if "SEARCH" in state["decision"]:
        return "search"
    return "skip"


# -----Build the graph-----
# register the shared state type and then add every node function above as a names node in the graph
graph = StateGraph(AgentState)

graph.add_node("caption", caption_node)
graph.add_node("vision_analysis", vision_analysis_node)
graph.add_node("decide", decision_node)
graph.add_node("search", search_node)
graph.add_node("report", report_node)

#the graph always starts at 'caption' for every image
graph.set_entry_point("caption")

#fixed edges: always run in this order, regardless of any decision
graph.add_edge("caption", "vision_analysis")
graph.add_edge("vision_analysis", "decide")

#conditional edge: after 'decide', route decision picks which key below to follow
graph.add_conditional_edges(
    "decide",
    route_decision,
    {
        "search": "search",
        "skip": "report",
    },
)

#both branches converge here: search always lead to report, and report is always the last step before the graph ends
graph.add_edge("search", "report")
graph.add_edge("report", END)

#compile graph into a runnable agent
agent = graph.compile()


if __name__ == "__main__":
    #manual test run
    result = agent.invoke({"image_path": "../landscape.jpg"})
    print(result["final_report"])
