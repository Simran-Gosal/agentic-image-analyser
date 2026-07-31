# Requirements

## Functional requirements

1. The system must allow a user to upload an image through the streamlist interface
2. The system must generate a caption for the uploaded image using the PyTorch vision model (BLIP / ViT-GPT2).
3. The system must use an LLM (via Ollama) to decide, based on the caption, whether additional research is needed.
4. If additional research is needed, the system must call a web search tool to gather extra context.
5. If additional research is not needed, the system must skip directly to compiling the report.
6. The system must compile a final structured report combining the caption and any additional context gathered.
7. The system must display the final report to the user through the Streamlit interface.

## Non-Functional requirements

1. Reliability - the captioning model must produce coherent, grammatically sensible output (not a nonsensical output that in not relevant to the image uploaded).
2. Performance - a single image should be processed and return a report within a reasonable time on local hardware (target: under ~30 seconds, accounting for local LLM inference without a dedicated GPU).
3. Portability - the system must run entirely on local hardware without requiring a dedicated NVIDIA GPU, since this is a constraint of the development machine.
4. Cost - the system must not depend on a paid third-party LLM API for its core reasoning, since it self-hosts its LLM via Ollama.
5. Usability - the interface must require no technical knowledge to operate; a user should only need to upload an image and read the output.
6. Maintainability - the agent's tools (vision model, web search) should be structured as separate, swappable functions rather than tightly coupled code, so individual components can be improved independently.


## DID THE FINAL PROJECT MEET THE REQUIREMENTS?

## Functional Requirements
 
| # | Requirement | Met? |
|---|---|---|
| 1 | The system must allow a user to upload an image through the Streamlit interface | MET - confirmed via app.py, tested with multiple images |
| 2 | The system must generate a caption for the uploaded image using the PyTorch vision model (BLIP / ViT-GPT2) | MET using BLIP-large (vision_tool_refactored.py) |
| 3 | The system must use an LLM (via Ollama) to decide, based on the caption, whether additional research is needed | MET using llama3 via Ollama (decision_tool.py)  |
| 4 | If additional research is needed, the system must call a web search tool to gather extra context | MET using Tavily API (search_tool.py). Confirmed working end-to-end; SEARCH path tested via both CLI and Streamlit  |
| 5 | If additional research is not needed, the system must skip directly to compiling the report | MET - confirmed via test.jpg (SKIP path) |
| 6 | The system must compile a final structured report combining the caption and any additional context gathered | MET - report_node in agent_graph.py that compiled caption, detailed analysis, additional context into one report |
| 7 | The system must display the final report to the user through the Streamlit interface | MET - displayed via st.write(result["final_report"]) |
 
## Non-Functional Requirements
 
| # | Requirement | Met? |
|---|---|---|
| 1 | **Reliability** - the captioning model must produce coherent, grammatically sensible output (not a nonsensical output that is not relevant to the image uploaded) | PARTIALLY MET - output is always grammatically readable but not always factually reliable. Testing found hallucinations of locations and confident misidentification of small objects.  |
| 2 | **Performance** - a single image should be processed and return a report within a reasonable time on local hardware (target: under ~30 seconds, accounting for local LLM inference without a dedicated GPU) | TESTING!! |
| 3 | **Portability** - the system must run entirely on local hardware without requiring a dedicated NVIDIA GPU, since this is a constraint of the development machine | MET - developed and tested throughout on local hardware with no dedicated NVIDIA GPU |
| 4 | **Cost** - the system must not depend on a paid third-party LLM API for its core reasoning, since it self-hosts its LLM via Ollama | MET - all reasoning and vision analysis runs locally via Ollama and an external API used is Tavily's free-tier web search |
| 5 | **Usability** - the interface must require no technical knowledge to operate; a user should only need to upload an image and read the output | MET - Streamlit interface requires only a file upload; report displays automatically with no configuration needed by the end user.|
| 6 | **Maintainability** - the agent's tools (vision model, web search) should be structured as separate, swappable functions rather than tightly coupled code, so individual components can be improved independently | MET - each tool lives in its own file with a single clear function. Imported independently into agent_graph.py. Demonstrated later in practice: vision analysis tool added later without needing to rewrite the existing caption/decision/search tools |
