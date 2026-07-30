'''
agent_state.py
- defines the shared 'state' object that flows through every node in the LangGraph agent.
'''

#IMPORTS
from typing import TypedDict

'''
FIELD-BY-FIELD

- image_path:the files path of the image being analysed

- caption: the short BLIP-larger caption - set by caption_node

- vision_analysis: more detailed, location-aware Ollama (llava)

- decision: literal string 'SEARCH' or 'SKIP' - set by decision_node

- search_results: list of {title, contents, url} dicts from Tavily - only populated if
  graph took the SEARCH branch; left unset if SKIP
  
- final_report: the compiled, human-readable output - set last by report_node, combining
  all the above into the final result
'''

class AgentState(TypedDict):
    image_path: str
    caption: str
    vision_analysis: str
    decision: str
    search_results: list
    final_report: str
