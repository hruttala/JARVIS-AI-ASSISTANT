import requests

def generate_image(prompt: str, size: str = "512x512") -> str:
    print(f"[Ollama - generate_image] Prompt: {prompt} | Size: {size}")
    return f"(Mock Image for prompt: {prompt})"

def ask_ollama(prompt: str, model: str = "llama3") -> str:
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        response.raise_for_status()
        res_json = response.json()

        print("\nOllama Raw Response JSON:")
        print(res_json)

        if "message" in res_json and "content" in res_json["message"]:
            return res_json["message"]["content"].strip()
        elif "response" in res_json:
            return res_json["response"].strip()
        else:
            return "[No usable content found in response]"
    except Exception as e:
        return f"[Ollama error]: {e}"