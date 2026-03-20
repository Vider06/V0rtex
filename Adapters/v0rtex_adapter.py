#!/usr/bin/env python3
"""
V0RTEX Update Adapter — v0rtex_adapter.py
Lives in: GitHub/{branch}/Adapters/v0rtex_adapter.py
Executed from TEMP by the in-app updater after downloading the new v0rtex.py.

Role:
  1. Read meta JSON (passed as argv[1])
  2. Kill all V0RTEX-related processes
  3. Install/upgrade all required dependencies from requirements.txt
  4. Remove obsolete packages listed in .vx_meta/.deps_to_remove (if present)
  5. Rebuild V0rtex_System directory structure
  6. Restore data if keep_data=True and backup_path is set
  7. Show splash "V0RTEX IS UPDATING..." while working
  8. Launch v0rtex.py
  9. Self-delete this adapter + meta JSON

This script is intentionally self-contained (stdlib only for bootstrap).
"""
import os, sys, json, subprocess, shutil, time, tempfile, threading

# ── Read meta ────────────────────────────────────────────────────────────────
META_PATH = sys.argv[1] if len(sys.argv) > 1 else None
meta = {}
if META_PATH and os.path.isfile(META_PATH):
    try:
        with open(META_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        print(f"[ADAPTER] Could not read meta: {e}")

INSTALL_DIR  = meta.get("install_dir") or os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE   = meta.get("python_exe")  or sys.executable
OLD_VER      = meta.get("old_version", "?")
NEW_VER      = meta.get("new_version", "?")
BRANCH       = meta.get("branch", "Windows_Release")
KEEP_DATA    = meta.get("keep_data", True)
BACKUP_PATH  = meta.get("backup_path", "")
MANIFEST     = meta.get("manifest", {})

UTILS_DIR    = os.path.join(os.path.dirname(INSTALL_DIR), "v0rtex_utils")
META_DIR     = os.path.join(UTILS_DIR, ".vx_meta")
MAIN_SCRIPT  = os.path.join(INSTALL_DIR, "v0rtex.py")
DEPS_REMOVE  = os.path.join(META_DIR, ".deps_to_remove")
LOG_DIR      = os.path.join(UTILS_DIR, "debug_log", "update_log")

NW = {"creationflags": 0x08000000} if sys.platform == "win32" else {}

# ── Logging ───────────────────────────────────────────────────────────────────
_LOG_LINES = []
def log(msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    _LOG_LINES.append(line)
    print(line)
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        day = time.strftime("%Y%m%d")
        with open(os.path.join(LOG_DIR, f"adapter_{day}.log"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception: pass

# ── Splash window ─────────────────────────────────────────────────────────────
_splash_root = [None]
_splash_label = [None]

def _run_splash():
    try:
        import tkinter as tk
        r = tk.Tk()
        r.overrideredirect(True)
        r.configure(bg="#0d0d14")
        r.attributes("-topmost", True)
        sw, sh = r.winfo_screenwidth(), r.winfo_screenheight()
        W, H = 520, 160
        r.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")
        tk.Frame(r, bg="#cba6f7", height=3).pack(fill="x")
        tk.Label(r, text="V 0 R T E X", font=("Consolas", 22, "bold"),
                 bg="#0d0d14", fg="#cba6f7").pack(pady=(18, 4))
        lbl = tk.Label(r, text="⚡  IS UPDATING...  ⚡",
                       font=("Consolas", 12, "bold"), bg="#0d0d14", fg="#a6e3a1")
        lbl.pack()
        sub = tk.Label(r, text=f"v{OLD_VER}  →  v{NEW_VER}  ·  {BRANCH}",
                       font=("Consolas", 9), bg="#0d0d14", fg="#585b70")
        sub.pack(pady=4)
        _splash_root[0] = r
        _splash_label[0] = lbl
        # Animate label
        _frames = ["⚡  IS UPDATING...  ⚡", "✦  IS UPDATING...  ✦", "◈  IS UPDATING...  ◈"]
        _fi = [0]
        def _tick():
            if not _splash_root[0]: return
            _fi[0] = (_fi[0] + 1) % len(_frames)
            try: lbl.config(text=_frames[_fi[0]])
            except: pass
            r.after(500, _tick)
        r.after(500, _tick)
        r.mainloop()
    except Exception as e:
        print(f"[ADAPTER] Splash error: {e}")

_splash_thread = threading.Thread(target=_run_splash, daemon=True)
_splash_thread.start()
time.sleep(0.5)  # let splash render

# ── Step 1: Kill V0RTEX processes ─────────────────────────────────────────────
log("[ 1/6 ]  Killing V0RTEX processes...")
_scripts_to_kill = [
    "v0rtex.py", "v0rtex_reinstall.py", "v0rtex_uninstall.py",
    "v0rtex_updater.py", "v0rtex_recovery_ui.py",
]
killed = 0
try:
    import psutil
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmd = " ".join(proc.info.get("cmdline") or [])
            if any(s in cmd for s in _scripts_to_kill) and proc.pid != os.getpid():
                proc.kill()
                killed += 1
        except Exception: pass
    log(f"  ✓ Killed {killed} V0RTEX process(es) via psutil")
except ImportError:
    # Fallback: taskkill on Windows
    if sys.platform == "win32":
        for script in _scripts_to_kill:
            try:
                subprocess.run(
                    ["taskkill", "/F", "/FI", f"WINDOWTITLE eq *{script}*"],
                    capture_output=True, timeout=5, **NW)
            except Exception: pass
    time.sleep(1.5)
    log("  ~ psutil not available — used taskkill fallback")

time.sleep(0.8)

# ── Step 2: Remove obsolete deps ──────────────────────────────────────────────
log("[ 2/6 ]  Checking obsolete dependencies...")
if os.path.isfile(DEPS_REMOVE):
    try:
        with open(DEPS_REMOVE, "r", encoding="utf-8") as f:
            to_remove = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        for pkg in to_remove:
            try:
                r = subprocess.run(
                    [PYTHON_EXE, "-m", "pip", "uninstall", "-y", pkg],
                    capture_output=True, text=True, timeout=60, **NW)
                log(f"  {"✓" if r.returncode == 0 else "~"} removed {pkg}")
            except Exception as e:
                log(f"  ~ {pkg}: {e}")
        os.remove(DEPS_REMOVE)
    except Exception as e:
        log(f"  ~ deps_to_remove error: {e}")
else:
    log("  ~ No .deps_to_remove file — skipping")

# ── Step 3: Install/upgrade requirements ─────────────────────────────────────
log("[ 3/6 ]  Installing/upgrading dependencies...")
req_path = os.path.join(INSTALL_DIR, "requirements.txt")
if os.path.isfile(req_path):
    try:
        r = subprocess.run(
            [PYTHON_EXE, "-m", "pip", "install", "-r", req_path,
             "--upgrade", "--prefer-binary", "-q", "--no-cache-dir",
             "--progress-bar", "off"],
            capture_output=True, text=True, timeout=300, **NW)
        if r.returncode == 0:
            log("  ✓ All dependencies installed/upgraded")
        else:
            log(f"  ~ pip warnings (non-fatal): {r.stderr[:120]}")
    except Exception as e:
        log(f"  ~ pip error: {e}")
else:
    log("  ~ requirements.txt not found — skipping")

# ── Step 4: Rebuild directory structure ──────────────────────────────────────
log("[ 4/6 ]  Rebuilding V0rtex_System directories...")
_required_dirs = [
    os.path.join(INSTALL_DIR, "rules"),
    os.path.join(INSTALL_DIR, "rules", "external"),
    os.path.join(INSTALL_DIR, "quarantine"),
    os.path.join(INSTALL_DIR, "reports"),
    os.path.join(INSTALL_DIR, "reports_pdf"),
    os.path.join(INSTALL_DIR, "backups"),
    os.path.join(INSTALL_DIR, "_recovery"),
    os.path.join(INSTALL_DIR, "sandbox_env"),
    os.path.join(INSTALL_DIR, "sandbox_env", "drop"),
    UTILS_DIR,
    META_DIR,
    LOG_DIR,
    os.path.join(UTILS_DIR, "debug_log", "crash_log"),
    os.path.join(UTILS_DIR, "debug_log", "session_log"),
    os.path.join(UTILS_DIR, "debug_log", "update_log"),
    os.path.join(UTILS_DIR, "Crash_Full_Report"),
]
for d in _required_dirs:
    try:
        os.makedirs(d, exist_ok=True)
    except Exception as e:
        log(f"  ~ Could not create {os.path.basename(d)}: {e}")
log("  ✓ Directories verified")

# ── Step 5: Write updated version metadata ───────────────────────────────────
log("[ 5/6 ]  Writing version metadata...")
try:
    vx_ver_path = os.path.join(META_DIR, "vx_version")
    with open(vx_ver_path, "w", encoding="utf-8") as f:
        json.dump({"version": NEW_VER, "name": "V0RTEX", "author": "Vider_06"}, f, indent=2)
    log(f"  ✓ vx_version → v{NEW_VER}")
except Exception as e:
    log(f"  ~ version write failed: {e}")

# ── Step 6: Launch V0RTEX ─────────────────────────────────────────────────────
log("[ 6/6 ]  Launching V0RTEX...")
time.sleep(0.5)

# Close splash
try:
    if _splash_root[0]:
        _splash_root[0].quit()
        _splash_root[0] = None
except Exception: pass

try:
    if os.path.isfile(MAIN_SCRIPT):
        subprocess.Popen([PYTHON_EXE, MAIN_SCRIPT], **NW)
        log(f"  ✓ V0RTEX v{NEW_VER} launched")
    else:
        log(f"  ✗ v0rtex.py not found at {MAIN_SCRIPT}")
except Exception as e:
    log(f"  ✗ Launch failed: {e}")

# ── Self-cleanup ──────────────────────────────────────────────────────────────
time.sleep(2.0)
log("  → Self-deleting adapter and meta files")
try:
    if META_PATH and os.path.isfile(META_PATH):
        os.remove(META_PATH)
except Exception: pass
try:
    os.remove(os.path.abspath(__file__))
except Exception: pass
