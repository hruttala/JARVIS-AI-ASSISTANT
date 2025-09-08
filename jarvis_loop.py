# jarvis_loop.py

import os
import time
import json
import subprocess
import importlib

def run_decomposer():
    print("\n🧠 [Step 1] Decomposing task into plan...")
    task = input("Describe the task (e.g. 'Create a landing page'): ").strip()

    decomposer = importlib.import_module("task_decomposer")
    plan = decomposer.generate_task_plan(task, save_to_file=True)

    print(f"\n✅ Plan saved to task_plan.json with {len(plan)} steps.")
    return plan

def run_executor(task_file):
    print(f"\n🚀 [Step 2] Executing task plan: {task_file}")
    executor = importlib.import_module("toolchain_executor")

    if "revised" in task_file:
        results, reasoning = executor.run_revised_plan(task_file)
    else:
        results, reasoning = executor.run_task_plan(task_file)

    return results, reasoning

def run_analyzer():
    print("\n📊 [Step 3] Analyzing results...")
    analyzer = importlib.import_module("task_analyzer")
    analyzer.analyze(auto_generate_revised_plan=True)

    # Check if revised_task_plan.json was created
    return os.path.exists("revised_task_plan.json")

def main_loop():
    run_decomposer()
    attempt = 1

    while True:
        print(f"\n=== 🧠 JARVIS AUTONOMOUS LOOP: Attempt {attempt} ===")
        results, reasoning = run_executor("revised_task_plan.json" if attempt > 1 else "task_plan.json")
        needs_retry = run_analyzer()

        if not needs_retry:
            print("\n🎉 All tasks completed successfully. No retries needed.")
            break

        print("\n🔁 Retrying failed steps in revised plan...")
        attempt += 1
        time.sleep(1)

    print("\n✅ JARVIS LOOP COMPLETE.")

if __name__ == "__main__":
    main_loop()