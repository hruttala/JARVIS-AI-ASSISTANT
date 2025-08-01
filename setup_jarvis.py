import os
import subprocess
import sys
import platform
import urllib.request
import zipfile
import shutil

# Required packages
REQUIRED_LIBRARIES = [
    "openai",
    "psutil",
    "edge-tts",
    "pydub",
    "colorama",
    "wikipedia",
    "SpeechRecognition",
    "python-dotenv",
]

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_DIR = "ffmpeg"

def run(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        sys.exit(1)

def create_venv():
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        run(f"{sys.executable} -m venv venv")

def install_dependencies():
    print("Installing required libraries...")
    pip = os.path.join("venv", "Scripts", "pip.exe")
    for lib in REQUIRED_LIBRARIES:
        run(f"{pip} install --upgrade {lib}")

def download_ffmpeg():
    if shutil.which("ffmpeg"):
        print("ffmpeg already installed.")
        return
    print("Downloading and installing ffmpeg...")
    zip_path = "ffmpeg.zip"
    urllib.request.urlretrieve(FFMPEG_URL, zip_path)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(FFMPEG_DIR)

    extracted_dir = next(os.scandir(FFMPEG_DIR)).path
    bin_path = os.path.join(extracted_dir, "bin")
    os.environ["PATH"] += os.pathsep + os.path.abspath(bin_path)

    print(f"ffmpeg installed and added to PATH: {bin_path}")
    os.remove(zip_path)

def main():
    create_venv()
    install_dependencies()
    download_ffmpeg()
    print("\n=== Jarvis Setup Complete ===")
    launch = input("Jarvis is ready. Do you want to launch it now? (Y/n): ").strip().lower()
    if launch in ["", "y", "yes"]:
        run("venv\\Scripts\\python.exe jarvis.py")

if __name__ == "__main__":
    main()
