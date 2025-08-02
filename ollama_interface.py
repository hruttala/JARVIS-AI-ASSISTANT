# ollama_interface.py

import requests

def ask_ollama(prompt: str) -> str:
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "mistral",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("message", {}).get("content", "[No content returned]")
    except Exception as e:
        return f"[Ollama HTTP error]: {e}"