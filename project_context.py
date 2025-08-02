import os
import shutil
import subprocess
import fitz  # PyMuPDF
import requests
from project_loader import (
    set_active_project,
    load_memory,
    save_memory
)

def speak(text):
    print("[JARVIS PROJECT]", text)

# ========== Project Setup ==========
def create_project_folder(name):
    path = os.path.join(os.getcwd(), name)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "main.py"), "w") as f:
        f.write(f"# {name} main file\n\n")
    speak(f"Created project folder: {name}")
    return path

def is_tool_installed(tool_name):
    return shutil.which(tool_name) is not None

def search_file(filename, search_path="C:\\"):
    for root, _, files in os.walk(search_path):
        if filename.lower() in [f.lower() for f in files]:
            return os.path.join(root, filename)
    return None

def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception as e:
        speak(f"Failed to read PDF: {e}")
        return ""

def summarize_with_ollama(text):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": f"Summarize this project report in a few key bullet points:\n{text}",
            "stream": False
        })
        summary = response.json().get("response", "Could not summarize.")
        speak("Here’s a quick summary of your project report:")
        speak(summary[:500])
    except Exception as e:
        speak(f"Could not summarize with Ollama: {e}")

# ========== File Interaction ==========
def list_project_files(path, extensions=(".py", ".js", ".html", ".css")):
    files = []
    for root, _, filenames in os.walk(path):
        for fname in filenames:
            if fname.endswith(extensions):
                rel_path = os.path.relpath(os.path.join(root, fname), path)
                files.append(rel_path)
    return files

def read_file(filepath):
    if not os.path.exists(filepath):
        speak("That file does not exist.")
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        speak(f"Reading contents of {os.path.basename(filepath)}")
        print("\n" + content[:500])
    except Exception as e:
        speak(f"Error reading file: {e}")

def summarize_code(filepath):
    if not os.path.exists(filepath):
        speak("That file does not exist.")
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        prompt = f"Summarize what this code does:\n{content}"
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        summary = response.json().get("response", "Could not summarize code.")
        speak(summary[:500])
    except Exception as e:
        speak(f"Error summarizing file: {e}")

def edit_code_file(filepath, instruction):
    if not os.path.exists(filepath):
        speak("That file does not exist.")
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            original_code = f.read()
        prompt = f"Here is a file:\n{original_code}\n\nPlease edit it to: {instruction}\nReturn only the modified code."
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        updated_code = response.json().get("response", None)
        if updated_code:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_code)
            speak("The file has been updated successfully.")
        else:
            speak("I didn’t receive valid updated code.")
    except Exception as e:
        speak(f"Error editing file: {e}")

def get_active_file_path():
    return "D:/Jarvis/sales.csv"        

# ========== Voice-Driven Project Creation ==========
def start_project_conversation():
    memory = load_memory()

    speak("What would you like to call this project?")
    project_name = input("Project name: ").strip()

    speak("What is this project about?")
    description = input("Description: ").strip()

    speak("What type of app is it? CLI, Web, or GUI?")
    app_type = input("Type: ").strip().lower()

    speak("Which language will you be using? Python, JS, etc.")
    language = input("Language: ").strip()

    speak("Do you have a project report file I should analyze? (yes/no)")
    if input("Has report? ").strip().lower() == "yes":
        speak("What is the filename?")
        filename = input("File name: ").strip()
        speak("Searching for the file. Please wait...")
        found_path = search_file(filename)
        if found_path:
            speak(f"Found the file at {found_path}. Reading it now...")
            report = extract_text_from_pdf(found_path) if found_path.endswith(".pdf") else open(found_path, "r", encoding="utf-8").read()
            summarize_with_ollama(report)
        else:
            report = ""
            speak("I couldn't find that file anywhere on your system.")
    else:
        report = ""

    # ✅ NOW create the project folder and set it
    path = create_project_folder(project_name)
    set_active_project(project_name, path)
    memory = load_memory()

    speak("Checking if VS Code is installed...")
    if not is_tool_installed("code"):
        speak("VS Code is not found. Please install it from https://code.visualstudio.com")
    else:
        subprocess.Popen(["code", path], shell=True)
        speak("Opening VS Code...")

    # ✅ Now it's safe to use those variables
    memory.setdefault("projects", []).append({
        "name": project_name,
        "description": description,
        "type": app_type,
        "language": language,
        "path": path,
        "report": report[:300]
    })
    save_memory(memory)
    speak("Project setup complete. Ready for development.")