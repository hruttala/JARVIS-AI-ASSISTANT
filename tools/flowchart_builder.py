# flowchart_builder.py

import subprocess
from pathlib import Path
from ollama_interface import ask_ollama


# -------------------------------
# 1. Convert input to Mermaid code using LLM
# -------------------------------
def generate_mermaid_diagram(input_text: str) -> str:
    prompt = f"""
Convert the following description or code into a valid Mermaid flowchart. Use 'flowchart TD' and return only the Mermaid syntax.

INPUT:
{input_text}

OUTPUT:
"""
    response = ask_ollama(prompt)
    return response.strip()


# -------------------------------
# 2. Render Mermaid to SVG (via mermaid-cli)
# -------------------------------
def render_mermaid_to_svg(mermaid_code: str, output_path: str = "flowchart.svg"):
    temp_input = "temp_mermaid.mmd"
    with open(temp_input, "w") as f:
        f.write(mermaid_code)

    try:
        subprocess.run(["mmdc", "-i", temp_input, "-o", output_path], check=True)
        print(f"[✅] SVG saved to: {Path(output_path).absolute()}")
    except subprocess.CalledProcessError:
        print("[❌] Failed to render with mermaid-cli. Is it installed globally?")
    finally:
        Path(temp_input).unlink(missing_ok=True)


# -------------------------------
# 3. Entry Point
# -------------------------------
def create_flowchart(input_text: str, render_svg: bool = False, output_path: str = "flowchart.svg"):
    mermaid_code = generate_mermaid_diagram(input_text)

    print("\n[🧠 Mermaid Code]")
    print(mermaid_code)

    if render_svg:
        render_mermaid_to_svg(mermaid_code, output_path)

    return mermaid_code


# -------------------------------
# 4. Intent Router Integration
# -------------------------------
def generate_flowchart_from_intent(params: dict):
    input_text = params.get("input", "")
    render = params.get("render", False)
    output = params.get("output", "flowchart.svg")
    return create_flowchart(input_text, render_svg=render, output_path=output)