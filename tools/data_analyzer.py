# tools/data_analyzer.py

import os
import pandas as pd
from ollama_interface import ask_ollama
from project_context import get_active_file_path

def handle(user_input, context={}):
    """Emulates Excel/Sheets: analyzes a CSV file using AI."""

    file_path = get_active_file_path()
    if not file_path or not file_path.endswith(".csv") or not os.path.exists(file_path):
        return "No active CSV file selected or file not found."

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return f"Failed to read CSV file: {e}"

    preview = df.head(10).to_markdown(index=False)

    prompt = f"""You are a data analyst.

The user said: "{user_input}"

Here are the first 10 rows of the dataset:

{preview}

Based on this, analyze the data and give trends, summaries, or insights.
If possible, recommend a chart or visual to go with the analysis.
Only use what you can infer from the visible data.
"""
    print("==== CSV Preview ====")
    print(preview)
    print("==== Prompt ====")
    print(prompt)

    response = ask_ollama(prompt)
    return response