# TECHNICAL ARCHITECTURE 

# TECH STACK

| LAYER |  TOOL  | REASONING |
|-------|-----|-------|
| Vision Model | PyTorch (via BLIP/VIT-GPT2, Hugging Face) | Pretrained image captioning. |
| Reasoning LLM | Ollama  | Self-hosted, runs locally without a dedicated NVIDIA GPU, responsible for deciding which tool to call, in what order, and when the task is complete.  |
| Agent Orchestration | LangGraph | Defines the workflow as a graph, letting the LLM decides the path dynamically rather than following one fixed sequence |
| Search Tool | Web Search API | Provides additional context when the caption alone isnt sufficient. |
| Interface | Streamlit | When a user uploads an image views the final structured report. |
