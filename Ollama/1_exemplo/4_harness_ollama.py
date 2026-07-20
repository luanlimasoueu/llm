#!/usr/bin/env python3
import json
import os
import subprocess
import urllib.error
import urllib.request

# Endpoint OpenAI-compatible que o Ollama expõe localmente.
# Não precisa de API key. Ajuste o host:porta se rodar remoto/docker.
API = os.getenv("OLLAMA_API", "http://localhost:11434/v1/chat/completions")

SYSTEM = """You are a CLI assistant with one tool: run_bash.
Use it whenever you need to inspect files or run commands.
Never claim you ran a command unless you actually called the tool.
After each tool call, read stdout, stderr, and returncode before deciding what to do next.
Ask before destructive commands unless the user explicitly asked for them."""

# Mesmo formato de function-calling da OpenAI, mas sem "strict" (extensão
# própria da OpenAI que o Ollama não entende / pode rejeitar).
TOOLS = [{
    "type": "function",
    "function": {
        "name": "run_bash",
        "description": "Run a bash command on the user's computer and return stdout, stderr, and returncode.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The exact bash command to run."}
            },
            "required": ["command"],
            "additionalProperties": False,
        },
    },
}]


def load_env(path=".env"):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def api(payload):
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"Ollama API error {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Não consegui conectar em {API}. O Ollama está rodando? (`ollama serve`)"
        ) from e


def run(command):
    try:
        p = subprocess.run(
            ["bash", "-lc", command],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return json.dumps({
            "stdout": p.stdout,
            "stderr": p.stderr,
            "returncode": p.returncode,
        })
    except subprocess.TimeoutExpired:
        return json.dumps({"stdout": "", "stderr": "timeout", "returncode": -1})


def chat(history):
    while True:
        r = api({
            "model": os.getenv("OLLAMA_MODEL", "llama3.1"),
            "messages": [{"role": "system", "content": SYSTEM}] + history,
            "tools": TOOLS,
        })

        message = r["choices"][0]["message"]
        history.append(message)

        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            print(f"\nassistant> {message.get('content', '').strip()}\n")
            return

        for call in tool_calls:
            command = json.loads(call["function"]["arguments"])["command"]
            print(f"\n$ {command}")
            output = run(command)
            result = json.loads(output)
            if result["stdout"]:
                print(result["stdout"], end="" if result["stdout"].endswith("\n") else "\n")
            if result["stderr"]:
                print(result["stderr"], end="" if result["stderr"].endswith("\n") else "\n")

            # No formato Chat Completions, a resposta da tool volta como
            # uma mensagem role="tool" referenciando o tool_call_id.
            history.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": output,
            })


def main():
    load_env()
    history = []
    print("Digite sua mensagem (Ctrl+C para sair).")
    while True:
        try:
            user_input = input("\nvocê> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input.strip():
            continue
        history.append({"role": "user", "content": user_input})
        chat(history)


if __name__ == "__main__":
    main()


#OLLAMA_MODEL=qwen2.5-coder:7b python3 4_harness_ollama.py