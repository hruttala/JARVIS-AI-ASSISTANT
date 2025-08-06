# file_generator.py

import json
import yaml
from pathlib import Path
from ollama_interface import ask_ollama


# ----------------------------------------
# 1. Generate content for a given file type
# ----------------------------------------
def generate_file_content(prompt: str, file_type: str) -> str:
    template = {
        "json": f"Generate a well-structured JSON file for the following:\n\n{prompt}\n\nRespond with valid JSON only.",
        "yaml": f"Generate a YAML config file for:\n\n{prompt}\n\nRespond with only YAML content.",
        "md": f"Write a Markdown file for the following project:\n\n{prompt}\n\nRespond in clean Markdown.",
        "txt": f"Write a text file for the following description:\n\n{prompt}",
        "env": f"Generate an .env file with keys and values for:\n\n{prompt}\n\nFormat: KEY=VALUE per line.",
        "py": f"Write a Python script for:\n\n{prompt}",
        "sh": f"Write a shell script to accomplish:\n\n{prompt}",
        "toml": f"Generate a TOML config file for:\n\n{prompt}"
    }

    task_prompt = template.get(file_type.lower(), f"Write a plain text file for:\n\n{prompt}")
    response = ask_ollama(task_prompt)
    return response.strip()


# ----------------------------------------
# 2. Save content to file
# ----------------------------------------
def write_file(filename: str, content: str):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[📄] File saved: {path.resolve()}")


# ----------------------------------------
# 3. Main interface
# ----------------------------------------
def create_file(prompt: str, file_type: str = "txt", filename: str = None) -> str:
    content = generate_file_content(prompt, file_type)

    if not filename:
        safe_name = prompt.lower().replace(" ", "")[:20].strip("")
        filename = f"{safe_name}.{file_type}"

    write_file(filename, content)
    return filename


# ----------------------------------------
# 4. Jarvis intent integration
# ----------------------------------------
def generate_file_from_intent(params: dict) -> str:
    prompt = params.get("prompt", "")
    file_type = params.get("type", "txt")
    filename = params.get("filename", None)
    return create_file(prompt, file_type, filename)