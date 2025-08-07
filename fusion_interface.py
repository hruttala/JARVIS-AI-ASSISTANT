# fusion_interface.py

"""
Fusion Interface
----------------
Interface layer for launching fusion tasks from Jarvis's voice or text command.
"""

from tool_fusion_engine import run_fusion_task
from fusion_logger import log_summary
from datetime import datetime


def start_fusion_task(user_input: str) -> str:
    """
    Launches a fusion task from a high-level instruction.
    Returns full result log.
    """
    print(f"\n🧠 Starting Fusion Task: {user_input}")
    print("⏳ Parsing steps and invoking tools...\n")

    result = run_fusion_task(user_input)

    print("\n✅ Fusion Task Complete!")
    print("📜 Recent Log:")
    print(log_summary())

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n=== Fusion Task @ {timestamp} ===\n"
    return header + result + "\n"