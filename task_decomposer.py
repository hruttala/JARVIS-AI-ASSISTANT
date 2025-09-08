# task_decomposer.py

import json

TOOL_MAP = {
    "design UI": "ui_designer",
    "generate image": "poster_generator",
    "write content": "content_writer",
    "analyze data": "data_analyzer",
    "write code": "code_editor",
    "summarize file": "summarizer",
}

def decompose_task(prompt):
    """
    Decomposes a high-level prompt into a list of subtasks.
    """
    # Simple rule-based mock breakdown — can plug into LLM later
    prompt = prompt.lower()

    subtasks = []
    if "landing page" in prompt:
        subtasks.append(("design UI", "Create a layout for the landing page"))
        subtasks.append(("write content", "Generate heading, subheading, and CTA text"))
        subtasks.append(("generate image", "Make hero banner image for the page"))
    elif "poster" in prompt:
        subtasks.append(("generate image", "Design poster graphic"))
        subtasks.append(("write content", "Generate caption and title text"))

    return subtasks


def map_to_tools(subtasks):
    """
    Maps subtasks to the tools available.
    """
    task_plan = []
    for action, description in subtasks:
        tool = TOOL_MAP.get(action, "manual")  # fallback
        task_plan.append({
            "tool": tool,
            "action": action,
            "description": description,
        })
    return task_plan


def generate_task_plan(prompt, save_to_file=True):
    subtasks = decompose_task(prompt)
    task_plan = map_to_tools(subtasks)

    if save_to_file:
        with open("task_plan.json", "w") as f:
            json.dump(task_plan, f, indent=2)

    return task_plan


if __name__ == "__main__":
    user_prompt = input("Describe the task: ")
    plan = generate_task_plan(user_prompt)
    print(json.dumps(plan, indent=2))