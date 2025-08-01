import json
import os
from datetime import datetime

Goal_FILE = "goals.json"

#----------------Load & Save-----------------
def load_goals():
    if not os.path.exists(Goal_FILE):
        return []
        with open(Goal_FILE, "r") as f:
            return json.load(f)
def save_goals(goals):
    with open(Goal_FILE, "w") as f:
        json.dump(goals, f, indent=2)

#----------------Core functions-----------------
def add_goal(description, deadline=None):
    goals= load_goals()
    goals.append({
        "description": description,
        "deadline": deadline,
        "completed": False,
        "added_on": str(datetime.now().date())
    })
    save_goals(goals)
    return f"Added goal: '{description}'" + (f" (due {deadline})" if deadline else "")

def list_goals():
    goals = load_goals()
    if not goals:
        return "You have no goals at the moment."
    
    response = "Here are your current goals:\n"
    for i, g in enumerate(goals, 1):
        status = "✅" if g["completed"] else "🕒"
        line = f"{i}. {g['description']} {status}"
        if g.get("deadline"):
            line += f" (due {g['deadline']})"
        response += line + "\n"
    return response.strip()

def mark_goal_done(index):
    goals = load_goals()
    if 0 <= index < len(goals):
        goals[index]["completed"] = True
        save_goals(goals)
        return f"Marked goal #{index+1} as complete."
    else:
        return "Invalid goal number."

def check_progress():
    goals = load_goals()
    total = len(goals)
    done = sum(g["completed"] for g in goals)
    return f"You’ve completed {done} out of {total} goals."