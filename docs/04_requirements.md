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