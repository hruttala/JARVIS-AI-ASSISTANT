# tools/code_editor.py

import os
from ollama_interface import ask_ollama
from project_context import get_active_file_path

def handle(user_input, context={}):
    """Emulates Cursor: reads the active file and applies AI-based code edits or explanations."""
    
    file_path = get_active_file_path()

    if not file_path or not os.path.exists(file_path):
        return "No active file selected or file not found."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return f"Failed to read file: {e}"

    prompt = (
        f"You are an AI code assistant like Cursor.\n"
        f'The user said: "{user_input}"\n\n'
        "Here is the code file:\n\n"
        "python\n"
        f"{code}\n"
        "\n\n"
        "Please return the edited version of the file (if an edit is requested), "
        "or an explanation (if asked to explain).\n"
        "Respond only with the full updated code or explanation."
    )

    response = ask_ollama(prompt)
    return response