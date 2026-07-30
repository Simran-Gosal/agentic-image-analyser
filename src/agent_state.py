from typing import TypedDict

class AgentState(TypedDict):
    image_path: str
    caption: str
    vision_analysis: str
    decision: str
    search_results: list
    final_report: str
