from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch

# -----Phase 1-----
# Load GIT-large-coco (captioning-finetuned version)
processor = AutoProcessor.from_pretrained("microsoft/git-large-coco")
model = AutoModelForCausalLM.from_pretrained("microsoft/git-large-coco")

# -----Phase 2----- Load and prepare the same test image used for BLIP/BLIP-2
image = Image.open("test.jpg")
image = image.convert("RGB")

# -----Phase 3-----
# Generate caption (GIT only needs pixel_values, no text prompt)
pixel_values = processor(images=image, return_tensors="pt").pixel_values

with torch.no_grad():
    generated_ids = model.generate(
    pixel_values=pixel_values,
    max_length=80,
    num_beams=5,
    repetition_penalty=1.3,
    min_new_tokens=20
)

# -----Phase 4-----
# Decode to readable text
caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(caption)
