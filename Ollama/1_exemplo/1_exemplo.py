import ollama

response = ollama.chat(
    model="qwen2.5-coder:7b",
    messages=[{"role": "user", "content": "Olá, tudo bem?"}],
)

print(response["message"]["content"])