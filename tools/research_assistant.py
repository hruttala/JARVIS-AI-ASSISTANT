# research_assistant.py

from ollama_interface import ask_ollama


# ----------------------------------------
# 1. Answer a research question
# ----------------------------------------
def answer_question(question: str) -> str:
    prompt = f"""
You are an expert researcher. Provide a clear, concise, and accurate answer to the following question:

{question}

Respond with useful detail, examples if needed, and no fluff.
"""
    response = ask_ollama(prompt)
    print("\n[🔎 Answer]")
    print(response.strip())
    return response.strip()


# ----------------------------------------
# 2. Summarize a passage or text
# ----------------------------------------
def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following content in a concise and clear way. Use bullet points if appropriate.

CONTENT:
{text}
"""
    response = ask_ollama(prompt)
    print("\n[📝 Summary]")
    print(response.strip())
    return response.strip()


# ----------------------------------------
# 3. Intent integration
# ----------------------------------------
def research_assistant_from_intent(params: dict) -> str:
    if "question" in params:
        return answer_question(params["question"])
    elif "text" in params:
        return summarize_text(params["text"])
    else:
        return "❌ Error: No valid 'question' or 'text' provided for research."