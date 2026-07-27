import ollama

response = ollama.chat(model="llama3", messages=[{"role":"user", "content": "Tell me a fact about zebras"}])
print(response["message"]["content"])
