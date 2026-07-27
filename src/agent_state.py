from typing import TypedDict

class AgentState(TypedDict):
    image_path: str
    caption: str
    decision: str
    search_results: list
    final_report: str
