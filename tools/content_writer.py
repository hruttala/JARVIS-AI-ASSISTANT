# tools/content_writer.py

def handle(prompt, context={}):
    """Emulates a creative content writer using Ollama."""
    full_prompt = f"""You are a marketing content writer.

Create compelling copy for the following request:
"{prompt}"

Generate a headline, subheading, and short body copy suitable for a landing page or poster.
Use a persuasive and energetic tone."""
    
    from ollama_interface import ask_ollama
    return ask_ollama(full_prompt)

# ✅ Toolchain Compatibility
def run(description):
    print(f"[Content Writer] Running from toolchain_executor: {description}")
    return handle(description)