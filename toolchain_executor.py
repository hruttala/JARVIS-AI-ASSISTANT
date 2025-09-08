# toolchain_executor.py

import json
import importlib
import traceback

def execute_tool(tool_name, description):
    try:
        module = importlib.import_module(f"tools.{tool_name}")
        if hasattr(module, "run"):
            result = module.run(description)
            return result
        else:
            print(f"[WARN] Tool {tool_name} has no 'run()' method.")
            return None
    except ModuleNotFoundError:
        print(f"[ERROR] Tool '{tool_name}' not found.")
        return None
    except Exception as e:
        print(f"[ERROR] Failed running {tool_name}: {e}")
        traceback.print_exc()
        return None

def run_task_plan(filename="task_plan.json"):
    with open(filename, "r") as f:
        plan = json.load(f)

    results = []
    reasoning_log = []

    for index, step in enumerate(plan):
        tool = step["tool"]
        action = step["action"]
        description = step["description"]

        print(f"\n🔧 Running tool: {tool} → {description}")
        output = execute_tool(tool, description)

        if output is None or (isinstance(output, str) and not output.strip()):
            print(f"[Retry] Retrying {tool} for: {description}")
            output = execute_tool(tool, description)

            if output is None or (isinstance(output, str) and not output.strip()):
                print(f"[FAIL] Tool {tool} failed again. Skipping this step.")
                output = "[ERROR] Tool failed twice. No output."
               
        step_result = {
            "step": index + 1,
            "tool": tool,
            "description": description,
            "output": output
        }

        # Save main result
        results.append(step_result)

        # Save reasoning
        reasoning_log.append({
            "step": index + 1,
            "tool_used": tool,
            "why": f"Based on action '{action}', this tool was selected for: '{description}' (retried if needed)",
            "input": description,
            "output_summary": output[:300] if isinstance(output, str) else str(output)
        })

    return results, reasoning_log

def run_revised_plan(filename="revised_task_plan.json"):
    print(f"[Jarvis] Executing revised plan from {filename}")
    results, reasoning_log = run_task_plan(filename)

    # Save all results
    with open("task_results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open("reasoning_log.json", "w") as f:
        json.dump(reasoning_log, f, indent=2)

    print("\n✅ Task chain completed. Results saved to task_results.json and reasoning_log.json")
    return results, reasoning_log

if __name__ == "__main__":
    print("[Jarvis] Starting task execution...")
    results, reasoning_log = run_task_plan()