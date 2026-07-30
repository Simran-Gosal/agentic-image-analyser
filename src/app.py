'''
app.py

- the streamlit front end for the whole project
- wrapes agent_graphy.py's compiled agent in a simple upload and view interface, so the agent can actually be demoed
  rather than only run fom the command line.

- write together everything built earlier in the project and displays the structured result
'''

#IMPORTS
import streamlit as st
from PIL import Image
import tempfile
import os

from agent_graph import agent

st.set_page_config(page_title="Agentic Image Analyser")

st.title("AGENTIC IMAGE ANALYSER")
st.write(
    "Upload an image. An agent captions it, decides whether it needs extra research, and returns a structured report."
)

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_container_width=True)

    # Save to a temp file so the existing agent (which expects a file path) can use it unchanged
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.convert("RGB").save(tmp.name)
        tmp_path = tmp.name
    
    with st.spinner("Agent is analysing the image..."):
        try:
            result = agent.invoke({"image_path": tmp_path})
            st.subheader("Report")
            st.write(result["final_report"])

            with st.expander("Show raw caption"):
                st.write(result["caption"])

            with st.expander("Show agent decision"):
                st.write(result["decision"])
        except Exception as e:
            st.error(f"Something went wrong while processing the image: {e}")
        finally:
            os.remove(tmp_path)
