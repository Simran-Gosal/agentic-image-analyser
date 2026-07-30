'''
vision_tool_refactored.py

- reusable, function based version of vision_tool.py
- refactor wraps the same logic into a callable generate_caption function

'''
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import ollama

GRAMMAR_CLEANUP_PROMPT = '''Fix ONLY the grammar and sentence structure of the following image caption.
Do NOT add, remove, or change any factual content - do not introduce any new details,
objects, people, or locations that are not already present in the original caption.
Only correct grammatical errors so it reads as one natural, coherent sentence.

Caption: "{caption}"

Reply with only the corrected caption, nothing else.'''


def clean_caption_grammar(caption, model="llama3"):
    '''
    Lightweight grammar cleanup pass over BLIP's raw caption, using the same
    Ollama text model already used for decision-making. Deliberately
    constrained to grammar only - does not use vision, so it cannot add
    facts that weren't already in the raw caption; it can only rephrase.
    '''
    prompt = GRAMMAR_CLEANUP_PROMPT.format(caption=caption)
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.1}
    )
    return response["message"]["content"].strip()

'''
A .jpg file, at the raw level is just compressed bytes.
The processor's job is to convert images into a very specific numerical format
the model was trained to expect

- resizing the image to an exact pixel size
- converting pixels into numbers
- normaling these numbers

Therefore, processor = "translate real-world input into the exact numerical shape this specific model expects"
'''
#-----Phase 1: load the model and its matching processor once, at import time-----
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
generator = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def generate_caption(image_path):
    #-----Phase 2: load and prepare the image-----
    image = Image.open(image_path)
    image = image.convert("RGB")

    #-----Phase 3: convert image into model's expected input format, then generate a caption-----
    inputs = processor(image, return_tensors="pt")
    output_ids = generator.generate(
        **inputs,
        repetition_penalty=1.3,
        max_new_tokens=60,
        min_new_tokens=20,
        num_beams=5
    )

    #-----Phase 4: decode generated tokens back into readable text-----
    caption = processor.decode(output_ids[0], skip_special_tokens=True)
    print (caption)
    return caption
