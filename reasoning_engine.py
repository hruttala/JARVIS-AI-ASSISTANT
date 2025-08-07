# reasoning_engine.py

"""
Reasoning Engine
----------------
Analyzes current tool memory and determines what action Jarvis should take next.

Depends on:
tool_memory.py (for current context)
ollama_interface.py (for LLM reasoning)
"""

from tool_memory import get_all_memory
from ollama_interface import ask_ollama


def suggest_next_action(task_goal: str) -> str:
    """
    Uses Ollama to suggest the next tool or action based on current memory state
    and user's overall goal.
    """
    memory_snapshot = get_all_memory()

    prompt = f"""
You are Jarvis, an AI assistant coordinating multiple tools.

The user's high-level goal is:
"{task_goal}"

Here is the current memory (outputs from tools so far):
{memory_snapshot}

Based on this, suggest the **next action Jarvis should take**, or say "done" if nothing else is needed.

Respond in this format:
NEXT: <clear instruction or tool to call>
"""
    response = ask_ollama(prompt)
    return response.strip()