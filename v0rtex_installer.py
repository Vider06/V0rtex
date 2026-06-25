import sys
import subprocess
import platform
import os
import shutil
import stat
import time
import json
import threading
import itertools

REPO         = "https://github.com/Vider06/V0rtex.git"
INSTALL_DIR  = "V0RTEX"
MANIFEST_URL = "https://raw.githubusercontent.com/Vider06/V0rtex/main/Supported_os.json"
MIN_PYTHON   = (3, 12)
BOOTSTRAP_DEPS = ["requests>=2.31.0"]

W   = "\033[0m"
R   = "\033[91m"
G   = "\033[92m"
Y   = "\033[93m"
B   = "\033[94m"
M   = "\033[95m"
C   = "\033[96m"
DM  = "\033[90m"
BLD = "\033[1m"
CLR = "\033[2K\r"

def _c(color, text): return f"{color}{text}{W}"

def banner():
    os.system("")
    print()
    print(_c(M,  "    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗"))
    print(_c(M,  "    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝"))
    print(_c(B,  "    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝ "))
    print(_c(B,  "    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗ "))
    print(_c(C,  "     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗"))
    print(_c(C,  "      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝"))
    print()
    print(_c(DM, "    ─────────────────────────────────────────────────────"))
    print(_c(BLD+M, "      V0RTEX Installer") +
          _c(DM,    "  |  Vulnerability Oriented Recon Threat Exploitation eXaminer"))
    print(_c(DM, "    ─────────────────────────────────────────────────────"))
    print()

def log(msg):     print(f"  {_c(B,'[*]')} {msg}")
def ok(msg):      print(f"  {_c(G,'[+]')} {msg}")
def warn(msg):    print(f"  {_c(Y,'[!]')} {msg}")
def err(msg):     print(f"  {_c(R,'[X]')} {msg}")
def section(msg): print(f"\n  {_c(DM,'┌─')} {_c(BLD+C, msg)}\n  {_c(DM,'│')}")
def step(msg):    print(f"  {_c(DM,'├─')} {msg}")
def end():        print(f"  {_c(DM,'└─────')}\n")

class Spinner:
    FRAMES = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    def __init__(self, msg):
        self.msg   = msg
        self._stop = threading.Event()
        self._t    = threading.Thread(target=self._spin, daemon=True)
    def _spin(self):
        for f in itertools.cycle(self.FRAMES):
            if self._stop.is_set(): break
            sys.stdout.write(f"{CLR}  {_c(B, f)} {self.msg}")
            sys.stdout.flush()
            time.sleep(0.08)
    def __enter__(self):
        self._t.start(); return self
    def __exit__(self, *_):
        self._stop.set(); self._t.join()
        sys.stdout.write(CLR); sys.stdout.flush()

def animated_bar(label, steps, delay=0.03):
    width = 32
    for i in range(width + 1):
        filled = "█" * i
        empty  = "░" * (width - i)
        pct    = int((i / width) * 100)
        bar    = f"{_c(M, filled)}{_c(DM, empty)}"
        sys.stdout.write(f"{CLR}  {_c(DM,'├─')} {label}  [{bar}{_c(DM,']')}  {_c(BLD+C, f'{pct}%')}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(CLR)
    sys.stdout.flush()

def typewrite(msg, delay=0.018):
    for ch in msg:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def check_python():
    section("Python Environment")
    with Spinner("Detecting Python version..."):
        time.sleep(0.6)
    v = sys.version_info
    step(f"Detected  {_c(BLD, f'Python {v.major}.{v.minor}.{v.micro}')}")
    step(f"Executable  {_c(DM, sys.executable)}")
    if (v.major, v.minor) < MIN_PYTHON:
        err(f"V0RTEX requires Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+.")
        err("Download it from https://python.org/downloads/")
        end(); sys.exit(1)
    if v.minor >= 13:
        warn(f"Python {v.major}.{v.minor} is newer than the tested range (3.12). "
             "V0RTEX should work, but report any issues.")
    animated_bar("Validating environment", 1, delay=0.015)
    ok(f"Python {v.major}.{v.minor}.{v.micro} — OK")
    end()

def check_git():
    section("Git")
    with Spinner("Locating git binary..."):
        time.sleep(0.5)
    if shutil.which("git") is None:
        err("git not found in PATH.")
        err("Install git from https://git-scm.com/downloads and re-run.")
        end(); sys.exit(1)
    try:
        r = subprocess.run(["git", "--version"], capture_output=True, text=True)
        step(_c(G, r.stdout.strip()))
    except Exception as e:
        err(f"git check failed: {e}")
        end(); sys.exit(1)
    ok("git — OK")
    end()

def install_bootstrap():
    section("Bootstrap Dependencies")
    step("Installing minimum requirements for the V0RTEX setup wizard...")
    print()
    failed = []
    for pkg in BOOTSTRAP_DEPS:
        name = pkg.split(">=")[0]
        with Spinner(f"Installing {name}..."):
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pkg,
                     "--quiet", "--disable-pip-version-check"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                result = "ok"
            except subprocess.CalledProcessError:
                result = "fail"
                failed.append(name)
        if result == "ok":
            ok(f"  {name}")
        else:
            warn(f"  {name} — FAILED (V0RTEX wizard will retry on first launch)")
    print()
    if failed:
        warn(f"Some packages failed: {', '.join(failed)}")
    else:
        ok("Bootstrap complete.")
    step(_c(DM, "Note: all other dependencies (pefile, psutil, YARA, etc.) are installed"))
    step(_c(DM, "      by the V0RTEX setup wizard on first launch."))
    end()

def detect_os():
    s = platform.system().lower()
    if "windows" in s: return "windows"
    if "linux"   in s: return "linux"
    if "darwin"  in s: return "macos"
    return None

def get_branch(os_type):
    return {
        "windows": "Windows_Release",
        "linux":   "Linux_Release",
        "macos":   "Macos_Release",
    }.get(os_type, "main")

def fetch_manifest():
    try:
        import requests
        r = requests.get(MANIFEST_URL, timeout=6)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def show_platform_info():
    section("Platform Detection")
    with Spinner("Detecting host OS..."):
        time.sleep(0.5)
    os_type = detect_os()
    if not os_type:
        err("Unsupported or unrecognised operating system.")
        end(); sys.exit(1)
    step(f"OS detected:  {_c(BLD+G, os_type.upper())}")

    with Spinner("Fetching build manifest from GitHub..."):
        manifest = fetch_manifest()

    STATUS_COLOR = {"Released": G, "Not Stable": Y, "Work in Progress": R}
    if manifest and os_type in manifest:
        info   = manifest[os_type]
        status = info.get("status", "Unknown")
        notes  = info.get("notes", "")
        color  = STATUS_COLOR.get(status, W)
        step(f"Build status: {_c(color+BLD, status)}")
        step(f"Notes:        {_c(DM, notes)}")
    else:
        warn("Could not fetch manifest — continuing with local defaults.")

    branch = get_branch(os_type)
    step(f"Target branch:{_c(M+BLD, f'  {branch}')}")
    end()
    return os_type

def check_disk_space():
    section("System Checks")
    with Spinner("Checking available disk space..."):
        time.sleep(0.4)
        try:
            free_mb = shutil.disk_usage(".").free // (1024 * 1024)
        except Exception:
            free_mb = None
    if free_mb is not None:
        color = G if free_mb > 500 else Y if free_mb > 100 else R
        step(f"Free disk space:  {_c(color+BLD, f'{free_mb:,} MB')}")
        if free_mb < 100:
            warn("Less than 100 MB free — installation may fail.")
    else:
        step("Disk space: could not determine")

    with Spinner("Checking network connectivity..."):
        try:
            import urllib.request
            urllib.request.urlopen("https://github.com", timeout=4)
            net_ok = True
        except Exception:
            net_ok = False
    if net_ok:
        step(f"Network:          {_c(G+BLD, 'Online')}  {_c(DM, '— github.com reachable')}")
    else:
        step(f"Network:          {_c(R+BLD, 'Offline or restricted')}")
        warn("Could not reach github.com — git clone may fail.")

    with Spinner("Scanning for existing V0RTEX processes..."):
        time.sleep(0.3)
        found = False
        try:
            import subprocess as _sp
            out = _sp.run(["tasklist" if os.name == "nt" else "ps", "aux"],
                          capture_output=True, text=True).stdout
            found = "v0rtex" in out.lower()
        except Exception:
            pass
    if found:
        warn("A V0RTEX process appears to be running — close it before continuing.")
    else:
        step(f"V0RTEX process:   {_c(G, 'Not running')}  {_c(DM,'— safe to proceed')}")

    end()

def force_remove_readonly(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def safe_delete(path):
    if not os.path.exists(path):
        return
    for attempt in range(3):
        try:
            if sys.version_info >= (3, 12):
                shutil.rmtree(path, onexc=force_remove_readonly)
            else:
                shutil.rmtree(path, onerror=force_remove_readonly)
            return
        except Exception as e:
            if attempt < 2:
                warn(f"Directory locked, retrying in 1s... ({e})")
                time.sleep(1)
            else:
                err(f"Failed to remove {path}: {e}")
                sys.exit(1)

def prepare():
    section("Installation Directory")
    target = os.path.abspath(INSTALL_DIR)
    step(f"Target path:  {_c(BLD, target)}")
    if os.path.exists(INSTALL_DIR):
        size_mb = sum(
            os.path.getsize(os.path.join(dp, f))
            for dp, _, files in os.walk(INSTALL_DIR)
            for f in files
        ) // (1024 * 1024)
        warn(f"Existing installation found ({size_mb} MB)")
        print()
        choice = input(f"  {_c(Y,'[?]')} Overwrite and reinstall? (y/n): ").strip().lower()
        print()
        if choice != "y":
            step("Keeping existing installation.")
            end()
            return "launch"
        with Spinner("Removing old installation..."):
            safe_delete(INSTALL_DIR)
        ok("Removed.")
    else:
        step(f"Status:       {_c(G, 'Ready')}  {_c(DM,'— directory is free')}")
    end()
    return "install"

def git_clone(branch):
    section("Downloading V0RTEX")
    step(f"Branch:  {_c(M+BLD, branch)}")
    step(f"Source:  {_c(DM, REPO)}")
    step(f"Target:  {_c(DM, os.path.abspath(INSTALL_DIR))}")
    print()
    animated_bar("Preparing clone", 1, delay=0.02)
    print()
    try:
        subprocess.run(
            ["git", "clone", "--depth=1", "-b", branch, REPO, INSTALL_DIR],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print()
        err(f"git clone failed: {e}")
        end(); sys.exit(1)
    print()
    animated_bar("Verifying download", 1, delay=0.015)
    print()

    entry = os.path.join(INSTALL_DIR, "v0rtex.py")
    if os.path.exists(entry):
        size_kb = os.path.getsize(entry) // 1024
        ok(f"v0rtex.py — {size_kb:,} KB")
    file_count = sum(len(files) for _, _, files in os.walk(INSTALL_DIR))
    ok(f"Download complete — {file_count} files")
    end()

def run_vortex():
    section("Launching V0RTEX")
    original_cwd = os.getcwd()
    os.chdir(INSTALL_DIR)

    entry = None
    for f in ["v0rtex.py", "main.py", "run.py"]:
        if os.path.exists(f):
            entry = f
            break

    if not entry:
        err("Could not find v0rtex.py in the installation directory.")
        os.chdir(original_cwd); end(); return

    step(f"Entry point:  {_c(G+BLD, entry)}")
    step(f"Python:       {_c(DM, sys.executable)}")
    print()

    for i in range(3, 0, -1):
        sys.stdout.write(f"{CLR}  {_c(DM,'├─')} {_c(Y, f'Starting in {i}...')}")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write(CLR); sys.stdout.flush()

    step(_c(G, "Handing off to V0RTEX setup wizard..."))
    end()
    time.sleep(0.3)

    try:
        subprocess.run([sys.executable, entry])
    except KeyboardInterrupt:
        print()
        warn("Interrupted.")
    finally:
        os.chdir(original_cwd)

def main():
    banner()

    sys.stdout.write("  ")
    typewrite(_c(Y,"[!]") + " This will install V0RTEX into " +
              _c(BLD, f"./{INSTALL_DIR}/"), delay=0.012)
    print(_c(DM, "      For educational and cybersecurity research use only."))
    print()
    proceed = input(f"  {_c(Y,'[?]')} Proceed with installation? (y/n): ").strip().lower()
    print()
    if proceed != "y":
        err("Installation aborted.")
        sys.exit(0)

    check_python()
    check_git()
    install_bootstrap()
    os_type = show_platform_info()
    check_disk_space()
    branch  = get_branch(os_type)
    action  = prepare()

    if action == "install":
        git_clone(branch)

    run_vortex()

    print()
    ok(_c(BLD, "V0RTEX installer finished. Have fun."))
    print()

if __name__ == "__main__":
    main()
