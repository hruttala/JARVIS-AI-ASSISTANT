import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    else:
        return {"projects": [], "active_project": None}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    print(f"[DEBUG] memory saved to {MEMORY_FILE}")
    print(f"[DEBUG] memory['active_project']: {memory.get('active_project')}")

# --- Active Project Management ---

def set_active_project(name, path):
    memory = load_memory()
    memory["active_project"] = {
        "name": name,
        "path": path,
        "last_file": None
    }
    save_memory(memory)
    print(f"[DEBUG] Setting active project: {name} at {path}")

def get_active_project():
    memory = load_memory()
    project = memory.get("active_project")
    print(f"[DEBUG] get_active_project -> {project}")
    return project

def list_all_projects():
    memory = load_memory()
    return memory.get("projects", [])

def get_project_tree(path, extensions=None):
    """
    Returns a list of all files (optionally filtered by extensions)
    Example:
        get_project_tree("D:/Jarvis/Drobe", [".py", ".js"])
    """
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if not extensions or any(filename.endswith(ext) for ext in extensions):
                rel_path = os.path.relpath(os.path.join(root, filename), path)
                files.append(rel_path)
    return sorted(files)

def set_last_file(filename):
    memory = load_memory()
    if memory.get("active_project"):
        memory["active_project"]["last_file"] = filename
        save_memory(memory)

def get_last_file():
    memory = load_memory()
    project = memory.get("active_project")
    if project:
        return project.get("last_file")
    return None