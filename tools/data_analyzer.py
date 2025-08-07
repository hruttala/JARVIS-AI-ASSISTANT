# tools/data_analyzer.py

import os
import pandas as pd
from ollama_interface import ask_ollama
from project_context import get_active_file_path

def analyze_data_from_intent(intent: str, data: str = "") -> str:
    print(f"[Data Analyzer] Analyzing data based on intent: {intent}")
    return "Analysis result based on intent: " + intent

def handle(user_input, context={}):
    file_path = get_active_file_path()

    if not file_path or not file_path.endswith(".csv") or not os.path.exists(file_path):
        return "No active CSV file selected or file not found."

    try:
        df = pd.read_csv(file_path)
        preview = df.head(5).to_string(index=False)
    except Exception as e:
        return f"Failed to read CSV file: {e}"

    prompt = f"""You are a data analyst.

The user said: "{user_input}"

Here is a preview of the dataset:

{preview}

Please summarize key insights in plain English.
"""
    response = ask_ollama(prompt)
    print("Ollama Response")
    print(response)
    return response