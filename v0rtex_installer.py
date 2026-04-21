import sys
import subprocess
import platform
import os
import shutil
import stat
import time

REPO = "https://github.com/Vider06/V0rtex.git"
INSTALL_DIR = "V0RTEX"

def log(msg):
    print(f"[+] {msg}")

def error(msg):
    print(f"[X] {msg}")

def ensure_requests():
    try:
        import requests
    except ImportError:
        log("requests not found → installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        log("requests installed")

def detect_os():
    os_name = platform.system().lower()
    if "windows" in os_name:
        return "windows"
    if "linux" in os_name:
        return "linux"
    if "darwin" in os_name:
        return "macos"
    return None

def get_branch(os_type):
    return {
        "windows": "Windows_Release",
        "linux": "Linux_Release",
        "macos": "MacOS_Release"
    }.get(os_type)

def force_remove_readonly(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def safe_delete(path):
    if not os.path.exists(path):
        return
    for _ in range(3):
        try:
            shutil.rmtree(path, onerror=force_remove_readonly)
            return
        except Exception as e:
            print(f"[!] retry delete: {e}")
            time.sleep(1)
    raise Exception("delete failed")

def prepare():
    if os.path.exists(INSTALL_DIR):
        print("[!] Existing installation detected")
        if input("Reinstall? (y/n): ").lower() != "y":
            return "launch"
        log("Cleaning old install...")
        safe_delete(INSTALL_DIR)
    return "install"

def git_clone(branch):
    log(f"Cloning {branch}")
    subprocess.run(
        ["git", "clone", "-b", branch, REPO, INSTALL_DIR],
        check=True
    )

def run_vortex():
    os.chdir(INSTALL_DIR)

    entry = None
    for f in ["v0rtex.py", "main.py", "run.py"]:
        if os.path.exists(f):
            entry = f
            break

    if not entry:
        error("No entry point found")
        return

    log(f"Running {entry}")
    subprocess.run([sys.executable, entry])

def main():
    log("V0RTEX Installer v2.2")

    ensure_requests()

    os_type = detect_os()
    if not os_type:
        error("Unsupported OS")
        return

    branch = get_branch(os_type)
    log(f"OS: {os_type}")
    log(f"Branch: {branch}")

    action = prepare()

    if action == "launch":
        run_vortex()
        return

    git_clone(branch)
    run_vortex()

    log("Done")

if __name__ == "__main__":
    main()