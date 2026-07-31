# Agentic Image Analyser 

---

An agentic system that captions images, autonomously decides whether they warrant further web research, returns a structure multi-part report - rather than just a single caption.

Built to explore what 'agentic' means in practice. Rather than a fixed pipeline, the system reasons its own output and decides for itself whether to take further action (searching the web) based on the content it sees.

## Table of Contents
- [What It Does](#what-it-does)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Testing & Findings](#testing--findings)
- [Known Limitations](#known-limitations)
- [What I'd Improve](#what-id-improve)

## What it does

1. upload an image via the Streamlit interface
2. BLIP-large (PyTorch/Transformers) generates a quick baseline caption
3. Ollama (llava), a locally run vision language model, produces a more detailed analysis - including an attempt to identify a specific location or landmark, if one is recognisable
4. Ollama (llama3) decides whether further research it needed (SEARCH) or the description is already self-contained (SKIP)
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

## Testing & Findings
This project was tested manually against a range of real images, and the process surfaces genuine, diagnosed issues along the way. 

Highlights include:
- **Location Hallucination**
- **Phantom-subject hallucination**
- **Non-Determinism**
- **Preprocessing sensitivity**

## Known Limitations


## What I'd Improve 


---
<div align=center>
  
**Simran Gosal | [GitHub](https://github.com/Simran-Gosal)**

</div>

