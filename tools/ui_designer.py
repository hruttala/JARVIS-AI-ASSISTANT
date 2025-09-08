# tools/ui_designer.py

def main(task, memory):
    print(f"[{__name__}] received task: {task}")
    return f"Output for: {task}"

def generate_ui_from_intent(intent: str) -> str:
    print(f"[UI Designer] Generating UI from intent: {intent}")
    return "<div class='product-card'>Generated Product Card UI</div>"

def handle(user_input, context={}):
    """Emulates a UI design tool like Figma."""
    prompt = f"""You are a UI designer assistant.

Design a mobile or web UI layout based on this user request:
"{user_input}"

Give a short description first, then output basic HTML (or React JSX) code if possible.
Avoid CSS unless necessary.
"""
    from ollama_interface import ask_ollama  # Ollama wrapper should exist
    response = ask_ollama(prompt)
    return response

# ✅ Toolchain Compatibility: Add run() for executor
def run(description):
    print(f"[UI Designer] Running from toolchain_executor: {description}")
    return handle(description)