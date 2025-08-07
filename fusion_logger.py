# fusion_logger.py

"""
Fusion Logger
-------------
Stores a timestamped log of fusion tasks, tool outputs, and reasoning steps.
Output is saved to fusion_log.json.
"""

import json
import os
from datetime import datetime

LOG_FILE = "fusion_log.json"


def load_log() -> list:
    """Loads the existing log from disk."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []


def save_log(log: list) -> None:
    """Saves the log list back to disk."""
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def log_fusion_step(task: str, tool: str, result: str, output: str = None) -> None:
    """
    Adds a single step entry to the log.
    """
    log = load_log()
    log.append({
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "tool": tool,
        "result": result,
        "output": output or "",
    })
    save_log(log)


def log_summary() -> str:
    """
    Returns a human-readable summary of recent steps.
    """
    log = load_log()
    if not log:
        return "No fusion log found."
    
    lines = []
    for entry in log[-10:]:  # Show last 10 steps
        time = entry['timestamp'].split("T")[-1][:8]
        lines.append(f"[{time}] {entry['tool']} → {entry['result']}")
    return "\n".join(lines)