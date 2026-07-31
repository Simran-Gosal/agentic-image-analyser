# Agentic Image Analyser 

---

An agentic system that captions images, autonomously decides whether they warrant further web research, returns a structured multi-part report - rather than just a single caption.

Built to explore what 'agentic' means in practice. Rather than a fixed pipeline, the system reasons its own output and decides for itself whether to take further action (searching the web) based on the content it sees.

## Table of Contents

- [What It Does](#what-it-does)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Usage](#usage)
- [Testing & Findings](#testing--findings)
- [Known Limitations](#known-limitations)
- [What I'd Improve](#what-id-improve)

## What it does

1. upload an image via the Streamlit interface
2. BLIP-large (PyTorch/Transformers) generates a quick baseline caption
3. Ollama (llava), a locally run vision language model, produces a more detailed analysis - including an attempt to identify a specific location or landmark, if one is recognisable
4. Ollama (llama3) decides whether further research is needed (SEARCH) or the description is already self-contained (SKIP)
5. If SEARCH, Tavily runs a real web search and pulls in genuine, sourced content.
6. everything is compiled into a structured report: Caption -> Detailed Analysis -> Additional Context

The whole pipeline is run locally - no dedicated GPU required, no paid LLM API for reasoning/vision steps.

## Architecture 

The core orchestration is built with LangGraph, using conditional routing so the agent takes a different path through the graph depending on what it decides.

## Tech Stack
 
| Area | Technology |
|---|---|
| Vision captioning | PyTorch, Hugging Face Transformers, BLIP-large |
| Agent orchestration | LangGraph |
| Local LLM inference | Ollama (llama3 for decision-making, llava for detailed vision analysis) |
| Web search | Tavily API |
| Interface | Streamlit |
| Language | Python |

## Setup

**Prerequisites**

- Python 3.10+
- Ollama installed locally with models pulled:
  - ollama pull llama3
  - ollama pull llava
- A free [Tavily](https://tavily.com) API key

### Setup Steps

1. git clone https://github.com/Simran-Gosal/agentic-image-analyser.git
2. cd agentic-image-analyser
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. create a '.env' file in the project root with: TAVILY_API_KEY=your_key_here

## Usage

- run a StreamLit interface
  - cd src
  - streamlit run app.py
- Upload an image in the browser - the agent will caption it, analyse it, decide whether to research further and display the full report.

*or run agent directly from the command line*
  cd src
  python agent_graph.py

**(Edit the 'image_path' at the bottom of 'agent_graph.py' to point at a different test image.)**

## Testing & Findings

This project was tested manually against a range of real images, and the process surfaces genuine, diagnosed issues along the way. 

Highlights include:

- **Location Hallucination**: earlier versions on BLIP-2 confidently invented a false, specific location for an image with no basis for the claim. This factored in choosing BLIP-large instead
- **Phantom-subject hallucination**: BLIP-large persistently describes a person in an image where none exists.
- **Non-Determinism**: the SEARCH/SKIP decision could flip between identical runs at default temperature - fixed by lowering it.
- **Preprocessing sensitivity**: the same image produced different, factually different captions depending on how it was encoded before reaching the model - fixed by preserving original upload bytes rather than re-encoding.

## Known Limitations

1. No automated pytest suite - testing is manual, documented in docs/06_Testing.md
2. Vision models can still confidently misidentify small/occluded objects
3. Web search relevance currently depends on the detailed vision analysis alone, not the initial caption
4. Small, manually chosen test image set rather than a large representative sample

## What I'd Improve 

- Automated test suite covering the core tools
- Combine both vision outputs (caption & detailed analysis) into the search query
- Lower the vision analysis temperature for more consistent location identification, matching the fix already applied to the decision step.
- Reduce processing time by optimising the pipeline. Measured at 76-106 seconds per image, well over the ~30 second target. Potential bottleneck as 'llama3' called separately for grammar cleanup and decision steps. Combining these into a single call could improve efficiency.

---
<div align="center">
  
**Simran Gosal | [GitHub](https://github.com/Simran-Gosal)**

</div>

