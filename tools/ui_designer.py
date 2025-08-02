# tools/ui_designer.py

def handle(user_input, context={}):
    """Emulates a UI design tool like Figma."""
    prompt = f"""You are a UI designer assistant.

Design a mobile or web UI layout based on this user request:
"{user_input}"

Give a short description first, then output basic HTML (or React JSX) code if possible.
Avoid CSS unless necessary.
"""
    
    from ollama_interface import ask_ollama  # You should have this as your Ollama wrapper
    response = ask_ollama(prompt)
    
    return response