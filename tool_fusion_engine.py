# tool_fusion_engine.py

"""
Tool Fusion Engine
------------------
Accepts high-level tasks, breaks them into subtasks, and calls the appropriate tools
using memory to chain their outputs.

Phases: 8-A to 8-G
"""

import importlib
import traceback
import json
import re

from tool_memory import set_memory, get_memory, get_all_memory
from fusion_logger import log_fusion_step
from ollama_interface import ask_ollama

# Mapping from tool names to Python module paths
TOOL_REGISTRY = {
    "ui_designer": "tools.ui_designer",
    "code_editor": "tools.code_editor",
    "poster_generator": "tools.poster_generator",
    # Add more tools as needed
}

def parse_fusion_plan(task: str) -> list:
    """
    Forcefully prompt Mistral to return tool-specific JSON steps only.
    """
    prompt = f"""
You are a planning assistant for a system that automates user goals.

The user said:
"{task}"

You MUST respond with ONLY a valid JSON list of steps for internal tools.

⚠️ DO NOT return shell commands, explanations, numbered steps, or markdown.
⚠️ DO NOT return anything except the JSON array.

Here is the correct format:

[
  {{ "tool": "ui_designer", "task": "Design a product card UI" }},
  {{ "tool": "code_editor", "task": "Generate HTML and CSS code for the UI" }},
  {{ "tool": "poster_generator", "task": "Create a promotional poster based on the design" }}
]

Only return a pure JSON list. No comments. No markdown. No CLI commands.
Allowed tools: {list(TOOL_REGISTRY.keys())}
"""

    response = ask_ollama(prompt).strip()

    # Clean markdown formatting if it sneaks in
    if " ''' " in response:
        match = re.search(r"'''(?:json)?\s*(.*?)'''", response, re.DOTALL)

        response = match.group(1).strip() if match else response

    try:
        array_match = re.search(r"\[\s*{.?}\s\]", response, re.DOTALL)
        if array_match:
            return json.loads(array_match.group(0))
        return []
    except Exception as e:
        print(f"[⚠️] Tool routing failed: {e}")
        return []
def call_tool(tool_name: str, task: str, memory_context: dict = {}) -> str:
    """
    Dynamically calls a tool module's main() function.
    """
    try:
        module_path = TOOL_REGISTRY[tool_name]
        tool_module = importlib.import_module(module_path)

        if hasattr(tool_module, "main"):
            output = tool_module.main(task=task, memory=memory_context)
            set_memory(f"{tool_name}_output", output)
            return f"[{tool_name}] ✅ Success"
        else:
            return f"[{tool_name}] ❌ No main() function found"
    except Exception as e:
        traceback.print_exc()
        return f"[{tool_name}] ❌ Error: {str(e)}"

def run_fusion_task(user_task: str) -> str:
    """
    Orchestrates multi-tool execution, memory sharing, and fallback handling.
    """
    steps = [
    { "tool": "ui_designer", "task": "Design a product card UI" },
    { "tool": "code_editor", "task": "Generate HTML and CSS code" },
    { "tool": "poster_generator", "task": "Create a promo poster for the UI" }
]
    if not steps:
        return "❌ Could not parse task into valid tool steps."

    results = []
    memory_snapshot = {}

    for step in steps:
        tool = step.get("tool")
        subtask = step.get("task")
        if not tool or not subtask:
            results.append("⚠️ Skipping invalid step.")
            continue

        print(f"➡️ {tool}: {subtask}")
        retries = 0
        max_retries = 1
        success = False

        while retries <= max_retries:
            output = call_tool(tool, subtask, memory_context=get_all_memory())
            tool_output = get_memory(f"{tool}_output")

            if "✅" in output:
                success = True
                break
            else:
                retries += 1
                print(f"⚠️ {tool} failed. Retry {retries}/{max_retries}")

        if not success:
            print(f"❌ {tool} failed after retries.")
            print("❓ Retry, skip, or stop?")
            choice = input("(r)etry / (s)kip / (x)stop > ").strip().lower()

            if choice == "r":
                retries = 0
                continue
            elif choice == "s":
                results.append(f"[{tool}] ❌ Skipped after failure")
                continue
            elif choice == "x":
                results.append("🛑 Fusion task stopped by user.")
                break

        results.append(output)
        log_fusion_step(task=subtask, tool=tool, result=output, output=tool_output)
        memory_snapshot[tool] = tool_output

    return "\n".join(results)