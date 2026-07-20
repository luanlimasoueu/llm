import requests

url = "http://localhost:11434/api/chat"
payload = {
    "model": "qwen2.5-coder:7b",
    "messages": [{"role": "user", "content": "Explique o que é o Ollama."}],
    "stream": False,
}

response = requests.post(url, json=payload)
print(response.json()["message"]["content"])
