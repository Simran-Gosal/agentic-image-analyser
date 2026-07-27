import ollama

DECISION_PROMPT = """You are deciding whether an image caption needs additional web research.

Caption: "{caption}"

Does this caption mention anything specific enough to warrant a web search for more context — such as a named landmark, a specific species, a notable object, or anything a person might want more real-world information about?

If YES, more context would genuinely help — reply with exactly one word: SEARCH
If NO, the caption is already sufficient on its own — reply with exactly one word: SKIP

Reply with only that single word, nothing else."""


def should_search(caption):
    prompt = DECISION_PROMPT.format(caption=caption)
    response = ollama.chat(model="llama3", messages=[
        {"role": "user", "content": prompt}],
        options={"temperature": 0.1}
    )
    decision = response["message"]["content"].strip()
    return decision


if __name__ == "__main__":
    # Test case 1: generic scene, should return SKIP
    test_caption_1 = "zebras drinking water from a small pond in the desert with rocks and grass around them, while another one is standing on the ground"
    print("Test 1 (generic scene):", should_search(test_caption_1))

    # Test case 2: named landmark, should return SEARCH
    test_caption_2 = "the Eiffel Tower at sunset"
    print("Test 2 (named landmark):", should_search(test_caption_2))
