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
        res_json = response.json()

        print("Ollama Raw Response JSON:")
        print(res_json)

        # Handle both formats
        if "message" in res_json and "content" in res_json["message"]:
            return res_json["message"]["content"]
        elif "response" in res_json:
            return res_json["response"]
        else:
            return "[No usable content found in response]"
    except Exception as e:
        return f"[Ollama error]: {e}"