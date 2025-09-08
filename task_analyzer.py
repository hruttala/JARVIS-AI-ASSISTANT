# task_analyzer.py

import os
import json
from pathlib import Path

def load_json(filename):
    if Path(filename).exists():
        with open(filename, "r") as f:
            return json.load(f)
    else:
        print(f"[Analyzer] File not found: {filename}")
        return []

def summarize_results(results):
    summary = []
    for step in results:
        tool = step.get("tool")
        output = step.get("output", "")
        success = "[ERROR]" not in output if isinstance(output, str) else bool(output)

        summary.append({
            "step": step["step"],
            "tool": tool,
            "status": "✅ Success" if success else "❌ Failed",
            "description": step.get("description"),
            "output_excerpt": output[:200] if isinstance(output, str) else str(output)
        })

    return summary

def suggest_improvements(summary):
    suggestions = []

    for step in summary:
        if step["status"] == "❌ Failed":
            suggestions.append(f"Retry or replace tool '{step['tool']}' for: {step['description']}")
        elif "poster" in step["description"].lower():
            suggestions.append(f"Consider using animation or background image for '{step['tool']}' poster.")
        elif "layout" in step["description"].lower():
            suggestions.append(f"Enhance UI layout by adding CSS or components library options.")

    if not suggestions:
        suggestions.append("No issues detected. Execution looks solid.")

    return suggestions

def analyze(auto_generate_revised_plan=True):
    results = load_json("task_results.json")
    reasoning = load_json("reasoning_log.json")

    print("\n📊 [Jarvis Analyzer] Task Chain Summary:\n")
    summary = summarize_results(results)

    for step in summary:
        print(f"Step {step['step']}: {step['tool']} → {step['status']}")
        print(f"  Task: {step['description']}")
        print(f"  Output: {step['output_excerpt']}\n")

    print("🧠 Suggestions / Improvements:")
    improvements = suggest_improvements(summary)
    for s in improvements:
        print(" -", s)

    output_data = {
        "summary": summary,
        "suggestions": improvements,
    }

    #Build revised plan for failed tests

    if auto_generate_revised_plan:
        revised_plan = []
        for step in summary:
            if step["status"] == "❌ Failed":
                revised_plan.append({
                    "tool": step["tool"],
                    "action": step["tool"],
                    "description": step["description"]
                })

        output_data["revised_plan"] = revised_plan

        if revised_plan:
            with open("revised_task_plan.json", "w") as f:
                json.dump(revised_plan, f, indent=2)
            print("\n♻️ Revised plan created with failed steps → saved to revised_task_plan.json"
                  )
        else:

            if os.path.exists("revised_task_plan.json"):
                os.remove("revised_task_plan.json")
            print("\n♻️ No failed steps, no revised plan needed.")

    #Save analysis
    with open("task_analysis.json", "w") as f:
        json.dump(output_data, f, indent=2)    

    print("\n✅ Analysis complete. Saved to task_analysis.json")

if __name__ == "__main__":
    analyze()