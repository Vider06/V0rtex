import sys
import subprocess
import platform
import os
import shutil
import stat
import time
import ast
import json

REPO = "https://github.com/Vider06/V0rtex.git"
INSTALL_DIR = "V0RTEX"
MANIFEST_URL = "https://raw.githubusercontent.com/Vider06/V0rtex/main/Supported_os.json"

def log(msg):
    print(f" [\033[94m*\033[0m] {msg}")

def success(msg):
    print(f" [\033[92m+\033[0m] {msg}")

def warning(msg):
    print(f" [\033[93m!\033[0m] {msg}")

def error(msg):
    print(f" [\033[91mX\033[0m] {msg}")

def ensure_requests():
    try:
        import requests
    except ImportError:
        log("Bootstrap requirement 'requests' missing. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
        success("Bootstrap pre-requisites secured.")

def fetch_manifest():
    log("Querying manifest server for remote build tracking...")
    import requests
    try:
        response = requests.get(MANIFEST_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            warning("Manifest synchronization failed (HTTP error). Operating in offline fallback.")
            return None
    except Exception as e:
        warning(f"Manifest link handshake failed: {e}. Defaulting to local mapping.")
        return None

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
    }.get(os_type, "main")

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
            if sys.version_info >= (3, 12):
                shutil.rmtree(path, onexc=force_remove_readonly)
            else:
                shutil.rmtree(path, onerror=force_remove_readonly)
            return
        except Exception as e:
            warning(f"Filesystem handle locked, retrying purge operation: {e}")
            time.sleep(1)
    raise Exception("Critical: Failed to flush existing sandbox directory environment.")

def prepare():
    if os.path.exists(INSTALL_DIR):
        print()
        warning("Active core instance directory collision detected.")
        choice = input("    Do you want to force-reinstall and overwrite current instance? (y/n): ").strip().lower()
        if choice != "y":
            return "launch"
        log("Purging old installation directories...")
        safe_delete(INSTALL_DIR)
        return "install"
    return "install"

def git_clone(branch):
    log(f"Establishing downstream mirror connection to target branch: \033[95m{branch}\033[0m...")
    try:
        subprocess.run(["git", "clone", "-b", branch, REPO, INSTALL_DIR], check=True, stdout=subprocess.DEVNULL)
        success("Module sequence source downloaded successfully.")
    except subprocess.CalledProcessError as e:
        error(f"Git execution sequence aborted with deployment error: {e}")
        sys.exit(1)

def run_vortex():
    original_cwd = os.getcwd()
    os.chdir(INSTALL_DIR)

    entry = None
    for f in ["v0rtex.py", "main.py", "run.py"]:
        if os.path.exists(f):
            entry = f
            break

    if not entry:
        error("Execution sequence halted: No suitable execution gateway (v0rtex.py/main.py) found.")
        os.chdir(original_cwd)
        return

    print("\n\033[90m--------------------------------------------------------\033[0m")
    success(f"Passing kernel thread handling to framework subsystem: \033[92m{entry}\033[0m")
    print("\033[90m--------------------------------------------------------\033[0m\n")
    time.sleep(1)
    
    try:
        subprocess.run([sys.executable, entry])
    except KeyboardInterrupt:
        print()
        warning("Subprocess termination signal received via execution matrix.")
    finally:
        os.chdir(original_cwd)

def main():
    os.system("")
    
    print("\033[95m    __      ______  _____ _______ ______   __   __\033[0m")
    print("\033[95m    \\ \\    / / __ \\|  __ \\__   __|  ____|  \\ \\ / /\033[0m")
    print("\033[94m     \\ \\  / / |  | | |__) | | |  | |__      \\ V / \033[0m")
    print("\033[94m      \\ \\/ /| |  | |  _  /  | |  |  __|      > <  \033[0m")
    print("\033[96m       \\  / | |__| | | \\ \\  | |  | |____    / . \\ \033[0m")
    print("\033[96m        \\/   \\____/|_|  \\_\\ |_|  |______|  /_/ \\_\\\033[0m")
    print("      \033[90m[⚡] SECURE DEPLOYMENT ENGINE v2.5_PRO [⚡]\033[0m\n")
    
    warning("Initialize system deployment sequence?")
    proceed = input("    Proceed? (y/n): ").strip().lower()
    if proceed != "y":
        print()
        error("Deployment execution aborted by user sequence.")
        sys.exit(0)
    print()

    ensure_requests()

    os_type = detect_os()
    if not os_type:
        error("Deployment matrix failed: Unmapped or hostile host Operating System environment.")
        return

    log(f"Host machine analysis: Local hardware architecture matches \033[92m{os_type.upper()}\033[0m.")

    manifest = fetch_manifest()
    if manifest and os_type in manifest:
        os_info = manifest[os_type]
        print(f"      \033[90m├─ Build Status :\033[0m {os_info.get('status', 'Unknown')}")
        print(f"      \033[90m└─ Release Notes:\033[0m {os_info.get('notes', 'None')}")
    print()

    branch = get_branch(os_type)
    action = prepare()

    if action == "install":
        git_clone(branch)
        
    run_vortex()
    print()
    success("Installer subsystem lifecycle routine closed. Execution clean.")

if __name__ == "__main__":
    main()
