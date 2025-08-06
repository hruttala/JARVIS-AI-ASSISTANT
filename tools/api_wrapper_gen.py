# api_wrapper_gen.py

from pathlib import Path
from ollama_interface import ask_ollama


# ----------------------------------------
# 1. Generate API wrapper code from prompt
# ----------------------------------------
def generate_api_wrapper(prompt: str, language: str = "python") -> str:
    lang_hint = {
        "python": "Use the 'requests' library and provide a class with methods for each endpoint.",
        "javascript": "Use 'fetch' and write in ES6 syntax.",
        "typescript": "Use 'axios' and TypeScript interfaces for responses."
    }

    full_prompt = f"""
Generate an API wrapper in {language.upper()} for the following request:

{prompt}

{lang_hint.get(language.lower(), '')}

Only output the code. Do not explain anything.
"""
    response = ask_ollama(full_prompt)
    return response.strip()


# ----------------------------------------
# 2. Save generated code to file
# ----------------------------------------
def write_wrapper_to_file(code: str, filename: str):
    Path(filename).write_text(code, encoding="utf-8")
    print(f"[📦] API wrapper saved to: {Path(filename).resolve()}")


# ----------------------------------------
# 3. One-shot wrapper generation + save
# ----------------------------------------
def create_api_wrapper(prompt: str, language: str = "python", filename: str = None) -> str:
    code = generate_api_wrapper(prompt, language)
    
    if not filename:
        safe = prompt.lower().replace(" ", "_")[:20]
        filename = f"{safe}_wrapper.{ 'py' if language == 'python' else 'js' }"

    write_wrapper_to_file(code, filename)
    return filename


# ----------------------------------------
# 4. Jarvis intent integration
# ----------------------------------------
def generate_api_wrapper_from_intent(params: dict) -> str:
    prompt = params.get("prompt", "")
    language = params.get("language", "python")
    filename = params.get("filename", None)
    return create_api_wrapper(prompt, language, filename)