import streamlit as st
from PIL import Image
import tempfile
import os

from agent_graph import agent

st.set_page_config(page_title="Agentic Image Analyser")

st.title("Agentic Image Analyser")
st.write(
    "Upload an image. An agent captions it, decides whether it needs"
    "extra research, and returns a structured report."
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
