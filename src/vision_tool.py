'''
vision_tool.py
- first working version of the image caption tool
- built using a flat, standalone script to prove that BLIP-large could generate captions
- before any of the agent/LangGraph structure existed


- not used by the pipeline
- file kept for reference only, to show original working version

- project moved to LangGraph, this was rewritten as a proper function in vision_tool_refactored.py
- this is what agent_graph.py imports and calls
'''

#IMPORTS
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

'''
A .jpg file, at the raw level is just compressed bytes.
The processor's job is to convert images into a very specific numerical format
the model was trained to expect

- resizing the image to an exact pixel size
- converting pixels into numbers
- normaling these numbers

Therefore, processor = "translate real-world input into the exact numerical shape this specific model expects"
'''

#-----Phase 1: load the model and it's matching processor-----
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
generator = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

#-----Phase 2: load and prepare the test image-----
image = Image.open("test.jpg")
image = image.convert("RGB")

#-----Phase 3: convert the image into the model's expected input format, then generate a caption-----
inputs = processor(image, return_tensors="pt")
output_ids = generator.generate(
    **inputs,
    #discourgaes the model from repeating the same words/phrases
    repetition_penalty=1.3,
    #upper limit on caption length
    max_new_tokens=60,
    #forces a minimum caption length 
    min_new_tokens=20,
    #beam search width - explores multiple candidate captions before picking the best one
    num_beams=5
)

#-----Phase 4: decode the generated tokens back into readable text-----
caption = processor.decode(output_ids[0], skip_special_tokens=True)
print (caption)
