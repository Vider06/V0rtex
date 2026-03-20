#!/usr/bin/env python3
"""
V0RTEX Update Adapter — v0rtex_adapter.py
Lives in: GitHub/{branch}/Adapters/v0rtex_adapter.py
Executed from TEMP by the in-app updater after downloading the new v0rtex.py.

Role:
  1. Read meta JSON (passed as argv[1])
  2. Kill all V0RTEX-related processes
  3. Install/upgrade all required dependencies
  4. Remove obsolete packages listed in .vx_meta/.deps_to_remove (if present)
  5. Rebuild V0rtex_System directory structure
  6. Write updated version metadata
  7. Show splash "V0RTEX IS UPDATING..." while working
  8. Launch v0rtex.py
  9. Self-delete adapter + meta JSON

This script is intentionally self-contained (stdlib + psutil optional).
Compatible with Python 3.8+.
"""
import os, sys, json, subprocess, shutil, time, tempfile, threading

# ── Platform flags ────────────────────────────────────────────────────────────
_WIN = sys.platform == "win32"
_MAC = sys.platform == "darwin"
# CREATE_NO_WINDOW — only pass on Windows, never on Linux/macOS
_POPEN_KW = {"creationflags": 0x08000000} if _WIN else {}

# ── Read meta ────────────────────────────────────────────────────────────────
META_PATH = sys.argv[1] if len(sys.argv) > 1 else None
meta = {}
if META_PATH and os.path.isfile(META_PATH):
    try:
        with open(META_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        print(f"[ADAPTER] Could not read meta: {e}")

INSTALL_DIR = meta.get("install_dir") or os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE  = meta.get("python_exe")  or sys.executable
OLD_VER     = meta.get("old_version", "?")
NEW_VER     = meta.get("new_version", "?")
BRANCH      = meta.get("branch", "Windows_Release")
KEEP_DATA   = meta.get("keep_data", True)
BACKUP_PATH = meta.get("backup_path", "")
MANIFEST    = meta.get("manifest", {})

UTILS_DIR   = os.path.join(os.path.dirname(INSTALL_DIR), "v0rtex_utils")
META_DIR    = os.path.join(UTILS_DIR, ".vx_meta")
MAIN_SCRIPT = os.path.join(INSTALL_DIR, "v0rtex.py")
DEPS_REMOVE = os.path.join(META_DIR, ".deps_to_remove")
LOG_DIR     = os.path.join(UTILS_DIR, "debug_log", "update_log")

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
    except Exception:
        pass

# ── Splash window (runs in daemon thread) ─────────────────────────────────────
# BUG FIX: use an Event so _run_splash can signal when mainloop is actually running,
# and _close_splash can call quit() safely from outside the thread.
_splash_ready  = threading.Event()
_splash_closed = threading.Event()
_splash_tk     = [None]   # holds the tk.Tk instance once mainloop starts

def _run_splash():
    try:
        import tkinter as tk
        r = tk.Tk()
        r.overrideredirect(True)
        r.configure(bg="#0d0d14")
        r.attributes("-topmost", True)

        sw = r.winfo_screenwidth()
        sh = r.winfo_screenheight()
        W, H = 520, 170
        r.geometry(f"{W}x{H}+{(sw - W) // 2}+{(sh - H) // 2}")

        tk.Frame(r, bg="#cba6f7", height=3).pack(fill="x")
        tk.Label(
            r, text="V 0 R T E X",
            font=("Consolas", 22, "bold"),    # BUG FIX: full tuple (name, size, weight)
            bg="#0d0d14", fg="#cba6f7"
        ).pack(pady=(18, 4))

        lbl = tk.Label(
            r, text="\u26a1  IS UPDATING...  \u26a1",
            font=("Consolas", 12, "bold"),
            bg="#0d0d14", fg="#a6e3a1"
        )
        lbl.pack()

        sub = tk.Label(
            r, text=f"v{OLD_VER}  \u2192  v{NEW_VER}  \u00b7  {BRANCH}",
            font=("Consolas", 9),
            bg="#0d0d14", fg="#585b70"
        )
        sub.pack(pady=4)

        # BUG FIX: store reference BEFORE signalling ready, but AFTER widget creation
        _splash_tk[0] = r

        _frames = [
            "\u26a1  IS UPDATING...  \u26a1",
            "\u2726  IS UPDATING...  \u2726",
            "\u25c8  IS UPDATING...  \u25c8",
        ]
        _fi = [0]

        def _tick():
            if _splash_closed.is_set():
                try: r.destroy()
                except Exception: pass
                return
            _fi[0] = (_fi[0] + 1) % len(_frames)
            try:
                lbl.config(text=_frames[_fi[0]])
            except Exception:
                pass
            r.after(500, _tick)

        # Signal ready BEFORE mainloop so caller doesn't wait forever
        r.after(0, _splash_ready.set)
        r.after(500, _tick)
        r.mainloop()

    except Exception as e:
        log(f"[ADAPTER] Splash error: {e}")
    finally:
        _splash_ready.set()   # unblock caller even if splash crashed
        _splash_closed.set()

def _close_splash():
    """Thread-safe splash close: set flag, let _tick() handle actual destroy."""
    _splash_closed.set()

# Start splash and wait up to 2s for it to be ready
_splash_thread = threading.Thread(target=_run_splash, daemon=True)
_splash_thread.start()
_splash_ready.wait(timeout=2.0)
time.sleep(0.2)

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
        except Exception:
            pass
    log(f"  \u2713 Killed {killed} V0RTEX process(es) via psutil")

except ImportError:
    # BUG FIX: WINDOWTITLE doesn't work for background Python scripts.
    # Use IMAGENAME + check cmdline via wmic/tasklist instead.
    if _WIN:
        try:
            # Get list of python.exe PIDs running our scripts via wmic
            r_wmic = subprocess.run(
                ["wmic", "process", "where",
                 "name='python.exe' or name='pythonw.exe'",
                 "get", "ProcessId,CommandLine", "/format:csv"],
                capture_output=True, text=True, timeout=10, **_POPEN_KW
            )
            for line in r_wmic.stdout.splitlines():
                parts = line.split(",")
                if len(parts) < 3:
                    continue
                cmdline = ",".join(parts[1:-1]).lower()
                pid_str = parts[-1].strip()
                if any(s.lower() in cmdline for s in _scripts_to_kill):
                    try:
                        pid = int(pid_str)
                        if pid != os.getpid():
                            subprocess.run(
                                ["taskkill", "/F", "/PID", str(pid)],
                                capture_output=True, timeout=5, **_POPEN_KW
                            )
                            killed += 1
                    except Exception:
                        pass
        except Exception as we:
            log(f"  ~ wmic failed: {we}")

    elif _MAC or not _WIN:
        # Linux/macOS: use pgrep + kill
        try:
            for script in _scripts_to_kill:
                r_pg = subprocess.run(
                    ["pgrep", "-f", script],
                    capture_output=True, text=True, timeout=5
                )
                for pid_line in r_pg.stdout.strip().splitlines():
                    try:
                        pid = int(pid_line.strip())
                        if pid != os.getpid():
                            os.kill(pid, 9)
                            killed += 1
                    except Exception:
                        pass
        except Exception as pe:
            log(f"  ~ pgrep failed: {pe}")

    time.sleep(1.0)
    log(f"  ~ psutil not available \u2014 killed {killed} process(es) via fallback")

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
                    capture_output=True, text=True, timeout=60, **_POPEN_KW
                )
                # BUG FIX: f-string with nested quotes crashes Python < 3.12
                # Use a pre-computed symbol instead.
                sym = "\u2713" if r.returncode == 0 else "~"
                log(f"  {sym} removed {pkg}")
            except Exception as e:
                log(f"  ~ {pkg}: {e}")
        os.remove(DEPS_REMOVE)
    except Exception as e:
        log(f"  ~ deps_to_remove error: {e}")
else:
    log("  ~ No .deps_to_remove file \u2014 skipping")

# ── Step 3: Install/upgrade requirements ─────────────────────────────────────
log("[ 3/6 ]  Installing/upgrading dependencies...")
req_path = os.path.join(INSTALL_DIR, "requirements.txt")
if os.path.isfile(req_path):
    try:
        r = subprocess.run(
            [PYTHON_EXE, "-m", "pip", "install", "-r", req_path,
             "--upgrade", "--prefer-binary", "-q", "--no-cache-dir",
             "--progress-bar", "off"],
            capture_output=True, text=True, timeout=300, **_POPEN_KW
        )
        if r.returncode == 0:
            log("  \u2713 All dependencies installed/upgraded")
        else:
            log(f"  ~ pip warnings (non-fatal): {r.stderr[:120]}")
    except Exception as e:
        log(f"  ~ pip error: {e}")
else:
    log("  ~ requirements.txt not found \u2014 skipping")

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
    os.path.join(INSTALL_DIR, "threat_feeds"),
    os.path.join(INSTALL_DIR, "pcap_dumps"),
    UTILS_DIR,
    META_DIR,
    LOG_DIR,
    os.path.join(UTILS_DIR, "debug_log", "crash_log"),
    os.path.join(UTILS_DIR, "debug_log", "session_log"),
    os.path.join(UTILS_DIR, "debug_log", "update_log"),
    os.path.join(UTILS_DIR, "debug_log", "trampoline_log"),
    os.path.join(UTILS_DIR, "debug_log", "admin_log"),
    os.path.join(UTILS_DIR, "debug_log", "setup_log"),
    os.path.join(UTILS_DIR, "debug_log", "recovery_ops"),
    os.path.join(UTILS_DIR, "Crash_Full_Report"),
]
for d in _required_dirs:
    try:
        os.makedirs(d, exist_ok=True)
    except Exception as e:
        log(f"  ~ Could not create {os.path.basename(d)}: {e}")
log("  \u2713 Directories verified")

# ── Step 5: Write updated version metadata ───────────────────────────────────
log("[ 5/6 ]  Writing version metadata...")
try:
    vx_ver_path = os.path.join(META_DIR, "vx_version")
    with open(vx_ver_path, "w", encoding="utf-8") as f:
        json.dump({"version": NEW_VER, "name": "V0RTEX", "author": "Vider_06"}, f, indent=2)
    log(f"  \u2713 vx_version \u2192 v{NEW_VER}")
except Exception as e:
    log(f"  ~ version write failed: {e}")

# ── Step 6: Launch V0RTEX ─────────────────────────────────────────────────────
log("[ 6/6 ]  Launching V0RTEX...")
time.sleep(0.6)

# Close splash before launching so it doesn't overlap
_close_splash()
time.sleep(0.3)

try:
    if os.path.isfile(MAIN_SCRIPT):
        # BUG FIX: don't pass creationflags=0 on non-Windows,
        # and use **_POPEN_KW which is {} on Linux/macOS
        subprocess.Popen([PYTHON_EXE, MAIN_SCRIPT], **_POPEN_KW)
        log(f"  \u2713 V0RTEX v{NEW_VER} launched")
    else:
        log(f"  \u2717 v0rtex.py not found at {MAIN_SCRIPT}")
except Exception as e:
    log(f"  \u2717 Launch failed: {e}")

# ── Self-cleanup ──────────────────────────────────────────────────────────────
time.sleep(2.0)
log("  \u2192 Self-deleting adapter and meta files")
try:
    if META_PATH and os.path.isfile(META_PATH):
        os.remove(META_PATH)
except Exception:
    pass
try:
    _self = os.path.abspath(__file__)
    # On Windows, can't delete a running script directly — rename then schedule
    if _WIN:
        _tmp_del = _self + ".del"
        os.rename(_self, _tmp_del)
        subprocess.Popen(
            ["cmd", "/c", f"ping 127.0.0.1 -n 3 >nul && del /f /q \"{_tmp_del}\""],
            creationflags=0x08000008,  # CREATE_NO_WINDOW | DETACHED_PROCESS
            close_fds=True
        )
    else:
        os.remove(_self)
except Exception:
    pass
