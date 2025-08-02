# === FILE: jarvis.py ===
import os
import json
import asyncio
import tempfile
import datetime
import webbrowser
import wikipedia
import speech_recognition as sr
import requests
import edge_tts
import subprocess
import re
import threading
import queue
import atexit
from colorama import Fore, Style
from project_context import (
    start_project_conversation,
    list_project_files,
    read_file,
    summarize_code,
    edit_code_file
)
from project_loader import (
    get_active_project,
    get_last_file,
    set_last_file,
    get_project_tree
)

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")
CHIME_FILE = "chime.mp3"
VOICE = "en-US-GuyNeural"
OLLAMA_MODEL = "mistral"
APP_SCAN_INTERVAL_DAYS = 3
SCAN_DIRS = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs")
]

# ---------------- MEMORY ----------------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

memory = load_memory()
user_name = memory.get("user", {}).get("name", "Sir")
memory.setdefault("goals", [])

# ---------------- SHUTDOWN HOOK ----------------
def shutdown_hook():
    memory["last_session"] = {
        "ended": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_command": memory.get("last_command", "Unknown")
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    print("[JARVIS] Session logged. See you next time, Hemanth.")

atexit.register(shutdown_hook)

# ---------------- AUDIO SYSTEM ----------------
def play_audio(file):
    subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", file],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_voice_sync(text):
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmpfile.close()
    asyncio.run(edge_tts.Communicate(text, VOICE).save(tmpfile.name))
    play_audio(tmpfile.name)
    os.remove(tmpfile.name)

voice_queue = queue.Queue()
def preload_voice_worker():
    while True:
        text = voice_queue.get()
        if text == "__exit__":
            break
        try:
            generate_voice_sync(text)
        except Exception as e:
            print("[Voice Error]", e)

threading.Thread(target=preload_voice_worker, daemon=True).start()

def speak(text, important=False):
    print(Fore.CYAN + f"[JARVIS] {text}" + Style.RESET_ALL)
    if important:
        chime()
    voice_queue.put(text)

def chime():
    if os.path.exists(CHIME_FILE):
        play_audio(CHIME_FILE)

# ---------------- GPT / LLM ----------------
def ask_gpt(prompt):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": f"You are Jarvis, Tony Stark's witty assistant. Respond concisely.\n{prompt}",
            "stream": False
        })
        return response.json().get("response", "I couldn’t generate a response, sir.")
    except Exception as e:
        return f"Ollama Error: {e}"

# ---------------- INPUT ----------------
def listen():
    print(Fore.YELLOW + "[Listening...]" + Style.RESET_ALL)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source, timeout=6)
            return r.recognize_google(audio)
        except:
            return None

def input_mode():
    speak("Listening for your command, sir.")
    for _ in range(2):
        text = listen()
        if text:
            return text
        speak("I didn’t catch that. Try again.")
    speak("Still nothing. Please type your command, sir.")
    return input("> ").strip()

# ---------------- GOALS ----------------
def add_goal(desc, deadline=None):
    memory["goals"].append({"description": desc, "deadline": deadline, "done": False})
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    return f"Goal added: {desc}" + (f" (Deadline: {deadline})" if deadline else "")

def list_goals():
    if not memory["goals"]:
        return "You have no goals yet."
    return "\n".join(
        [f"{i+1}. {'✅' if g['done'] else '❌'} {g['description']} ({g.get('deadline') or 'No deadline'})"
         for i, g in enumerate(memory["goals"])]
    )

def mark_goal_done(index):
    try:
        memory["goals"][index]["done"] = True
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)
        return f"Marked goal {index+1} as complete."
    except:
        return "Invalid goal number."

def check_progress():
    goals = memory["goals"]
    done = sum(1 for g in goals if g["done"])
    total = len(goals)
    return f"You've completed {done} of {total} goals ({(done/total)*100:.1f}%)." if total else "No goals yet."

# ---------------- APP SCANNING ----------------
def should_rescan_apps():
    try:
        last = datetime.datetime.fromisoformat(memory.get("last_app_scan", "2000-01-01"))
        return (datetime.datetime.now() - last).days >= APP_SCAN_INTERVAL_DAYS
    except:
        return True

def scan_for_apps():
    found = {}
    for folder in SCAN_DIRS:
        if not os.path.exists(folder): continue
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".exe"):
                    found[file.lower().replace(".exe", "")] = os.path.join(root, file)
    return found

def update_app_list():
    if not should_rescan_apps(): return
    memory["apps"] = scan_for_apps()
    memory["last_app_scan"] = datetime.datetime.now().isoformat()
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    speak(f"I’ve indexed {len(memory['apps'])} apps.", important=True)

# ---------------- COMMAND HANDLER ----------------
import difflib

def match_file_by_description(command):
    project = get_active_project()
    if not project:
        speak("No active project found.")
        return None
    all_files = get_project_tree(project["path"], extensions=(".py", ".js", ".html", ".css", ".json"))
    matches = difflib.get_close_matches(command, all_files, n=1, cutoff=0.4)
    if matches:
        matched = matches[0]
        speak(f"I believe you're referring to {matched}")
        set_last_file(matched)
        return os.path.join(project["path"], matched)
    else:
        speak("No matching file.")
        return None

def handle_command(command):
    command = command.lower()
    memory["last_command"] = command

    if "add goal" in command:
        speak("What goal?")
        desc = input("> ")
        speak("Deadline? (yes/no)")
        deadline = input("> ") if input("> ").lower() == "yes" else None
        speak(add_goal(desc, deadline)); return

    if "list goals" in command: speak(list_goals()); return
    if "progress" in command: speak(check_progress()); return
    if "mark goal" in command and "done" in command:
        speak("Which goal number?")
        try: speak(mark_goal_done(int(input("> "))-1))
        except: speak("Invalid number.")
        return

    if "start project" in command:
        start_project_conversation(); return

    if "list project files" in command:
        proj = get_active_project()
        if proj:
            files = list_project_files(proj["path"])
            speak("Here are the files:")
            for f in files: print("-", f)
        else: speak("No active project.")
        return

    if "list all" in command and "file" in command:
        proj = get_active_project()
        if not proj:
            speak("No active project."); return
        folder, ext = None, None
        ext_map = {
            "python": [".py"], "javascript": [".js"], "html": [".html"],
            "css": [".css"], "json": [".json"]
        }
        for key, exts in ext_map.items():
            if key in command: ext = exts
        for word in command.split():
            if "/" in word or "\\" in word:
                folder = word.strip("/\\")
            elif word in ["components", "src", "pages"]:
                folder = word
        files = get_project_tree(proj["path"], extensions=ext)
        if folder:
            files = [f for f in files if f.startswith(folder + os.sep)]
        speak("Here are the matching files:" if files else "No matching files.")
        for f in files: print("-", f)
        return

    for app, path in memory.get("apps", {}).items():
        if app in command:
            speak(f"Launching {app}", important=True)
            threading.Thread(target=os.startfile, args=(path,), daemon=True).start()
            return

    if "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query}...")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return

    if "read" in command:
        path = match_file_by_description(command)
        if path: read_file(path); return

    if "summarize" in command:
        path = match_file_by_description(command)
        if path: summarize_code(path); return

    if "edit" in command:
        path = match_file_by_description(command)
        instruction = command.split("edit")[-1].strip()
        if path:
            speak(f"Editing file based on: {instruction}")
            edit_code_file(path, instruction)
        return

    if "what's my name" in command:
        speak(f"Your name is {user_name}, sir."); return

    if "who is" in command or "what is" in command:
        try:
            topic = command.replace("who is", "").replace("what is", "").strip()
            speak(wikipedia.summary(topic, sentences=2))
        except:
            speak("I couldn’t find that, sir.")
        return

    speak(ask_gpt(command))

def split_and_handle(command):
    parts = re.split(r"\bthen\b|\band\b", command, flags=re.IGNORECASE)
    for part in parts:
        if part.strip():
            handle_command(part.strip())

# ---------------- MAIN ----------------
def main():
    update_app_list()
    speak(f"Systems online, {user_name}.")
    while True:
        command = input_mode()
        if not command: continue
        if "exit" in command or "shutdown" in command:
            chime(); speak("Shutting down. Goodbye."); break
        split_and_handle(command)

from intent_router import route_intent

if __name__ == "__main__":
    # TEMP: Phase 7 tool emulation test
    response = route_intent("Analyze this CSV and show the best performing category")
    print(response)

    # Run Jarvis loop normally after testing
    # main()

#if __name__ == "__main__":
    #main()