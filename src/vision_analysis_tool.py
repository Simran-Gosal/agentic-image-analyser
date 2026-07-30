'''
vision_analysis_tool.py

- added to solve two problems found once the pipeline was demoable:

1. report was too thin - BLIP-large only every produces a single short caption, so the 'final report' read as just one line
2. no way to actually attempt identifying a destination/location

This tool sends the raw image directly to a vision-capable Ollama model (llava), asking
for a longer, more detailed analysis - including explicit attempt at naming a location.
'''

#IMPORTS
import ollama

VISION_ANALYSIS_PROMPT = '''Look at this image carefully and provide a detailed analysis covering:
1. What is shown in the scene (subjects, setting, activity)
2. Any identifiable location, landmark, or destination - name it specifically if you recognise it
3. Notable visual details (weather, time of day, mood, style)

Be specific where you can, but do NOT guess a location with false confidence if you
are not sure - explicitly say "no specific location identifiable" if that's the case.

Keep the analysis to 4-6 sentences, written as plain prose (not a list).'''


def analyse_image(image_path, model="llava"):
    '''
    Send the image directly to a vision-capable Ollama model for detailed analysis.
    '''
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = ollama.chat(
        model=model,
        messages=[{
            "role": "user",
            "content": VISION_ANALYSIS_PROMPT,
            "images": [image_bytes],
        }],
        options={"temperature": 0.2},
    )
    return response["message"]["content"].strip()


if __name__ == "__main__":
    # Test with the landscape image - should attempt to identify it as Rainbow Mountain, Peru
    print(analyse_image("../landscape.jpg"))
