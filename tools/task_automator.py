# task_automator.py

import subprocess
import shlex
import os
from pathlib import Path
from datetime import datetime
from ollama_interface import ask_ollama


# ----------------------------
# 1. Run a single command
# ----------------------------
def run_command(command: str) -> dict:
    print(f"[▶] Running: {command}")
    try:
        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            shell=True if os.name == "nt" else False
        )
        return {
            "command": command,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except Exception as e:
        return {
            "command": command,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e)
        }


# ----------------------------
# 2. Handle multiple commands in a chain
# ----------------------------
def run_task_chain(commands: list[str], log_file: str = None) -> list[dict]:
    results = []
    for cmd in commands:
        result = run_command(cmd)
        results.append(result)

        if log_file:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"\n--- {datetime.now()} ---\n")
                f.write(f"$ {cmd}\n")
                f.write(f"Exit Code: {result['exit_code']}\n")
                f.write(f"STDOUT:\n{result['stdout']}\n")
                f.write(f"STDERR:\n{result['stderr']}\n")

    return results


# ----------------------------
# 3. Parse intent using LLM
# ----------------------------
def parse_commands_from_natural_text(task_description: str) -> list[str]:
    prompt = f"""
You are a CLI task planner. Convert the following task description into a list of shell commands.
Respond with plain text, one command per line.

TASK:
{task_description}

COMMANDS:
"""
    response = ask_ollama(prompt)
    return [line.strip() for line in response.strip().splitlines() if line.strip() and not line.startswith("#")]


# ----------------------------
# 4. Main entry point
# ----------------------------
def automate_tasks(task_description: str, log: bool = False, log_file: str = "task_log.txt") -> list[dict]:
    commands = parse_commands_from_natural_text(task_description)
    return run_task_chain(commands, log_file if log else None)


# ----------------------------
# 5. Jarvis Intent Integration
# ----------------------------
def run_automation_from_intent(params: dict):
    description = params.get("task", "")
    log = params.get("log", False)
    log_file = params.get("log_file", "task_log.txt")
    return automate_tasks(description, log=log, log_file=log_file)