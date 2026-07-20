#!/usr/bin/env python3
"""
Chat simples no terminal consumindo um modelo local rodando no Ollama.

Requisitos:
    - Ollama instalado e rodando (o app já sobe o servidor em localhost:11434)
    - Um modelo já baixado (ex: ollama pull qwen2.5-coder:14b)
    - Biblioteca requests: pip install requests

Uso:
    python3 chat_ollama.py
    python3 chat_ollama.py --model qwen2.5-coder:7b
"""

import argparse
import json
import sys
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


def check_ollama_running():
    """Verifica se o servidor do Ollama está de pé antes de começar."""
    try:
        requests.get("http://localhost:11434", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False


def stream_chat(model: str, messages: list):
    """Envia o histórico de mensagens e streama a resposta token a token."""
    payload = {"model": model, "messages": messages, "stream": True}

    with requests.post(OLLAMA_URL, json=payload, stream=True) as resp:
        if resp.status_code != 200:
            print(f"\n[Erro {resp.status_code}] {resp.text}")
            return ""

        full_reply = ""
        for line in resp.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            if chunk.get("done"):
                break
            content = chunk.get("message", {}).get("content", "")
            print(content, end="", flush=True)
            full_reply += content
        print()  # quebra de linha ao final da resposta
        return full_reply


def main():
    parser = argparse.ArgumentParser(description="Chat local via Ollama")
    parser.add_argument(
        "--model",
        default="qwen2.5-coder:7b",
        help="Nome do modelo já baixado (ex: qwen2.5-coder:7b)",
    )
    args = parser.parse_args()

    if not check_ollama_running():
        print("❌ Ollama não parece estar rodando. Abra o app do Ollama e tente de novo.")
        sys.exit(1)

    print(f"💬 Chat local com '{args.model}' — digite 'sair' para encerrar.\n")

    messages = []
    while True:
        try:
            user_input = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais!")
            break

        if user_input.lower() in ("sair", "exit", "quit"):
            print("Até mais!")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        print(f"{args.model}: ", end="", flush=True)
        reply = stream_chat(args.model, messages)

        if reply:
            messages.append({"role": "assistant", "content": reply})
        print()


if __name__ == "__main__":
    main()