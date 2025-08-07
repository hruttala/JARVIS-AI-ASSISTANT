# tool_memory.py

"""
Tool Memory Module
------------------
Stores and shares intermediate results between tools in Jarvis.

Used by: tool_fusion_engine, individual tools (UI Designer, Code Editor, etc.)
"""

import threading
import json

# Shared memory dictionary (thread-safe)
_tool_memory = {}
_lock = threading.Lock()

def set_memory(key: str, value: any) -> None:
    """Stores a value in tool memory with a unique key."""
    with _lock:
        _tool_memory[key] = value

def get_memory(key: str) -> any:
    """Retrieves a value from tool memory by key."""
    with _lock:
        return _tool_memory.get(key)

def delete_memory(key: str) -> None:
    """Deletes a key-value pair from tool memory."""
    with _lock:
        _tool_memory.pop(key, None)

def clear_memory() -> None:
    """Clears the entire tool memory."""
    with _lock:
        _tool_memory.clear()

def get_all_memory() -> dict:
    """Returns a copy of the current memory dictionary."""
    with _lock:

     from tool_memory import get_all_memory
     print("\n Final tool memory snapdhot:")
     print(json.dumps(get_all_memory(), indent=2))

    return dict(_tool_memory)