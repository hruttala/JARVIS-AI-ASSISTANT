import os
import json
import importlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPABILITIES_PATH = os.path.join(BASE_DIR, "tools_capabilities.json")

def load_capabilities():
    with open(CAPABILITIES_PATH, "r") as f:
        return json.load(f)

def route_intent(user_input: str, context: dict = {}):
    capabilities = load_capabilities()
    for tool_id, meta in capabilities.items():
        if not meta.get("active", True):
            continue
        for kw in meta["keywords"]:
            if kw.lower() in user_input.lower():
                module_name = meta["module"]
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, "handle"):
                        return module.handle(user_input, context)
                except Exception as e:
                    return f"[Tool '{tool_id}' failed to load]: {e}"
    return None  # Fallback to LLM or generic response