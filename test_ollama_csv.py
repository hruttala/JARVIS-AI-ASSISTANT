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
        print("✅ Raw JSON:")
        print(response.json())
        return response.json()["message"]["content"]
    except Exception as e:
        return f"[Ollama error]: {e}"

# Minimal CSV preview as plain text
preview = """Product,Sales
A,100
B,200"""

prompt = f"""You are a data analyst.

Here is a preview of the dataset:

{preview}

Please summarize the sales performance in plain English.
"""

response = ask_ollama(prompt)
print("🧠 Final Response:")
print(response)