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
#-----Phase 1-----
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
generator = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

#-----Phase 2-----
image = Image.open("test.jpg")
image = image.convert("RGB")

#-----Phase 3-----
inputs = processor(image, return_tensors="pt")
output_ids = generator.generate(
    **inputs,
    repetition_penalty=1.3,
    max_new_tokens=60,
    min_new_tokens=20,
    num_beams=5
)

#-----Phase 4-----
caption = processor.decode(output_ids[0], skip_special_tokens=True)
print (caption)
