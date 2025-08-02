# tools/presentation_creator.py

from ollama_interface import ask_ollama

def handle(user_input, context={}):
    """Creates a slide-style outline based on a topic using Ollama (PowerPoint-style)."""

    prompt = f"""You are an expert presentation designer.

The user asked: "{user_input}"

Please create a professional 5-slide presentation outline.
Each slide should include:
A title
2 to 4 bullet points
No slide numbers or HTML, just clean markdown

Format example:

# Slide Title
Bullet point 1
Bullet point 2

Only return the slide content.
"""

    response = ask_ollama(prompt)
    return response