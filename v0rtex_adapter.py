
import os, sys, json, subprocess, time, threading, re as _re

_WIN = sys.platform == "win32"
_MAC = sys.platform == "darwin"

META_PATH = sys.argv[1] if len(sys.argv) > 1 else None
meta: dict = {}
if META_PATH and os.path.isfile(META_PATH):
    try:
        with open(META_PATH, "r", encoding="utf-8") as _f:
            meta = json.load(_f)
    except Exception as _e:
        print(f"[ADAPTER] Cannot read meta: {_e}")

INSTALL_DIR: str = meta.get("install_dir") or os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE:  str = meta.get("python_exe")  or sys.executable
OLD_VER:     str = meta.get("old_version", "?")
NEW_VER:     str = meta.get("new_version", "?")
BRANCH:      str = meta.get("branch", "TESTING-GENERAL")
MANIFEST:    dict = meta.get("manifest", {})

UTILS_DIR   = os.path.join(os.path.dirname(INSTALL_DIR), "v0rtex_utils")
META_DIR    = os.path.join(UTILS_DIR, ".vx_meta")
MAIN_SCRIPT = os.path.join(INSTALL_DIR, "v0rtex.py")
DEPS_REMOVE = os.path.join(META_DIR, ".deps_to_remove")
LOG_DIR     = os.path.join(UTILS_DIR, "debug_log", "update_log")


def _run(cmd: list, timeout: int = 30, text: bool = False) -> "subprocess.CompletedProcess[str]":
    kw: dict = {"capture_output": True, "timeout": timeout}
    if text:
        kw["text"] = True
    if _WIN:
        kw["creationflags"] = 0x08000000
    return subprocess.run(cmd, **kw)


def _popen(cmd: list) -> "subprocess.Popen[bytes]":
    kw: dict = {}
    if _WIN:
        kw["creationflags"] = 0x08000000
    return subprocess.Popen(cmd, **kw)


def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        day = time.strftime("%Y%m%d")
        with open(os.path.join(LOG_DIR, f"adapter_{day}.log"), "a", encoding="utf-8") as _lf:
            _lf.write(line + "\n")
    except Exception:
        pass


def _detect_version_from_script(script_path: str) -> str:
    """
    Auto-detect the version embedded in v0rtex.py when new_version is unknown.
    Tries multiple patterns in order:
      1. The obfuscated join pattern:  ["0","9","9","X0"]
      2. The ADM_BADGE_W line:        "0.9.9",".X0  by
      3. Any dotted version literal:  "0.9.9.X0"
    Returns the detected version string, or "?" on failure.
    """
    try:
        with open(script_path, "r", encoding="utf-8", errors="replace") as _sf:

            _src = _sf.read(120_000)


        _m1 = _re.search(r'\["(\d+)","(\d+)","(\d+)","(X\d+)"\]', _src)
        if _m1:
            return f"{_m1.group(1)}.{_m1.group(2)}.{_m1.group(3)}.{_m1.group(4)}"


        _m2 = _re.search(r'"(\d+\.\d+\.\d+)","(\.[Xx]\d+)\s', _src)
        if _m2:
            return _m2.group(1) + _m2.group(2).strip()


        _m3 = _re.search(r'"(0\.\d+\.\d+\.X\d+)"', _src)
        if _m3:
            return _m3.group(1)

    except Exception as _de:
        log(f"  ~ version detect error: {_de}")

    return "?"



_ver_source = "meta"
if NEW_VER in ("?", "", None):
    log("  ~ new_version missing from meta — auto-detecting from v0rtex.py...")
    if os.path.isfile(MAIN_SCRIPT):
        NEW_VER = _detect_version_from_script(MAIN_SCRIPT)
        _ver_source = "script_autodetect"
        if NEW_VER == "?":

            NEW_VER = OLD_VER
            _ver_source = "fallback_old_ver"
    else:
        NEW_VER = OLD_VER
        _ver_source = "fallback_old_ver (no script)"

log(f"  ℹ  NEW_VER={NEW_VER}  (source: {_ver_source})")
log(f"  ℹ  OLD_VER={OLD_VER}  BRANCH={BRANCH}")



_splash_ready  = threading.Event()
_splash_closed = threading.Event()
_splash_tk: list = [None]


def _run_splash() -> None:
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
            font=("Consolas", 22, "bold"),
            bg="#0d0d14", fg="#cba6f7",
        ).pack(pady=(18, 4))

        lbl = tk.Label(
            r, text="\u26a1  IS UPDATING...  \u26a1",
            font=("Consolas", 12, "bold"),
            bg="#0d0d14", fg="#a6e3a1",
        )
        lbl.pack()

        tk.Label(
            r, text=f"v{OLD_VER}  \u2192  v{NEW_VER}  \u00b7  {BRANCH}",
            font=("Consolas", 9),
            bg="#0d0d14", fg="#585b70",
        ).pack(pady=4)

        _splash_tk[0] = r


        _frames = [
            "\u26a1  IS UPDATING...  \u26a1",
            "\u2726  IS UPDATING...  \u2726",
            "\u25c8  IS UPDATING...  \u25c8",
        ]
        _fi = [0]

        def _tick() -> None:
            if _splash_closed.is_set():
                try:
                    r.destroy()
                except Exception:
                    pass
                return
            _fi[0] = (_fi[0] + 1) % len(_frames)
            try:
                lbl.config(text=_frames[_fi[0]])
            except Exception:
                pass
            r.after(500, _tick)

        r.after(0, _splash_ready.set)
        r.after(500, _tick)
        r.mainloop()

    except Exception as _se:
        log(f"  ~ Splash error: {_se}")
    finally:
        _splash_ready.set()
        _splash_closed.set()


_splash_thread = threading.Thread(target=_run_splash, daemon=True)
_splash_thread.start()
_splash_ready.wait(timeout=2.0)
time.sleep(0.2)



log("[ 1/6 ]  Killing V0RTEX processes...")
_SCRIPTS = [
    "v0rtex.py", "v0rtex_reinstall.py", "v0rtex_uninstall.py",
    "v0rtex_updater.py", "v0rtex_recovery_ui.py",
]
_killed = 0

try:
    import psutil
    for _proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            _cmd = " ".join(_proc.info.get("cmdline") or [])
            if any(_s in _cmd for _s in _SCRIPTS) and _proc.pid != os.getpid():
                _proc.kill()
                _killed += 1
        except Exception:
            pass
    log(f"  \u2713 Killed {_killed} process(es) via psutil")

except ImportError:
    if _WIN:
        try:
            _r = _run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe",
                 "/FI", "IMAGENAME eq pythonw.exe", "/FO", "CSV", "/NH"],
                timeout=10, text=True,
            )
            for _line in _r.stdout.splitlines():
                _parts = _line.strip().strip('"').split('","')
                if len(_parts) < 2:
                    continue
                try:
                    _pid = int(_parts[1])
                except ValueError:
                    continue
                if _pid == os.getpid():
                    continue
                _wmic = _run(
                    ["wmic", "process", "where", f"ProcessId={_pid}",
                     "get", "CommandLine", "/format:list"],
                    timeout=5, text=True,
                )
                if any(_s.lower() in _wmic.stdout.lower() for _s in _SCRIPTS):
                    _run(["taskkill", "/F", "/PID", str(_pid)], timeout=5)
                    _killed += 1
        except Exception as _we:
            log(f"  ~ Kill fallback error: {_we}")
    else:
        for _script in _SCRIPTS:
            try:
                _r = subprocess.run(
                    ["pgrep", "-f", _script],
                    capture_output=True, text=True, timeout=5,
                )
                for _pid_line in _r.stdout.strip().splitlines():
                    try:
                        _pid = int(_pid_line.strip())
                        if _pid != os.getpid():
                            os.kill(_pid, 9)
                            _killed += 1
                    except Exception:
                        pass
            except Exception:
                pass
    time.sleep(1.0)
    log(f"  ~ psutil unavailable \u2014 killed {_killed} process(es) via fallback")

time.sleep(0.8)



log("[ 2/6 ]  Checking obsolete dependencies...")
if os.path.isfile(DEPS_REMOVE):
    try:
        with open(DEPS_REMOVE, "r", encoding="utf-8") as _f:
            _to_remove = [_l.strip() for _l in _f if _l.strip() and not _l.startswith("#")]
        for _pkg in _to_remove:
            try:
                _r = _run([PYTHON_EXE, "-m", "pip", "uninstall", "-y", _pkg], timeout=60, text=True)
                _sym = "\u2713" if _r.returncode == 0 else "~"
                log(f"  {_sym} removed {_pkg}")
            except Exception as _e:
                log(f"  ~ {_pkg}: {_e}")
        os.remove(DEPS_REMOVE)
    except Exception as _e:
        log(f"  ~ deps_to_remove error: {_e}")
else:
    log("  ~ No .deps_to_remove \u2014 skipping")



log("[ 3/6 ]  Installing/upgrading dependencies...")
_req_path = os.path.join(INSTALL_DIR, "requirements.txt")
if os.path.isfile(_req_path):
    try:
        _r = _run(
            [PYTHON_EXE, "-m", "pip", "install", "-r", _req_path,
             "--upgrade", "--prefer-binary", "-q", "--no-cache-dir",
             "--progress-bar", "off"],
            timeout=300, text=True,
        )
        if _r.returncode == 0:
            log("  \u2713 All dependencies installed/upgraded")
        else:
            log(f"  ~ pip warnings: {_r.stderr[:120]}")
    except Exception as _e:
        log(f"  ~ pip error: {_e}")
else:
    log("  ~ requirements.txt not found \u2014 skipping")



log("[ 4/6 ]  Rebuilding directory structure...")
_REQUIRED_DIRS = [
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
    UTILS_DIR, META_DIR, LOG_DIR,
    os.path.join(UTILS_DIR, "debug_log", "crash_log"),
    os.path.join(UTILS_DIR, "debug_log", "session_log"),
    os.path.join(UTILS_DIR, "debug_log", "trampoline_log"),
    os.path.join(UTILS_DIR, "debug_log", "admin_log"),
    os.path.join(UTILS_DIR, "debug_log", "update_log"),
    os.path.join(UTILS_DIR, "debug_log", "setup_log"),
    os.path.join(UTILS_DIR, "debug_log", "recovery_ops"),
    os.path.join(UTILS_DIR, "Crash_Full_Report"),
]
for _d in _REQUIRED_DIRS:
    try:
        os.makedirs(_d, exist_ok=True)
    except Exception as _e:
        log(f"  ~ {os.path.basename(_d)}: {_e}")
log("  \u2713 Directories OK")



log("[ 5/6 ]  Writing version metadata...")
try:
    _vx_version_path = os.path.join(META_DIR, "vx_version")



    if NEW_VER in ("?", "", None):
        log("  ~ NEW_VER still unknown — preserving existing vx_version (no overwrite)")
    else:
        with open(_vx_version_path, "w", encoding="utf-8") as _vf:
            json.dump({"version": NEW_VER, "name": "V0RTEX", "author": "Vider_06"}, _vf, indent=2)
        log(f"  \u2713 vx_version \u2192 v{NEW_VER}  (was: v{OLD_VER})")
except Exception as _e:
    log(f"  ~ version write failed: {_e}")



log("[ 6/6 ]  Launching V0RTEX...")
time.sleep(0.5)
_splash_closed.set()
time.sleep(0.3)

try:
    if os.path.isfile(MAIN_SCRIPT):
        _popen([PYTHON_EXE, MAIN_SCRIPT])
        log(f"  \u2713 V0RTEX v{NEW_VER} launched")
    else:
        log(f"  \u2717 v0rtex.py not found: {MAIN_SCRIPT}")
except Exception as _e:
    log(f"  \u2717 Launch failed: {_e}")



time.sleep(2.0)
log("  \u2192 Cleaning up...")
try:
    if META_PATH and os.path.isfile(META_PATH):
        os.remove(META_PATH)
except Exception:
    pass
try:
    _self = os.path.abspath(__file__)
    if _WIN:
        _tmp = _self + ".del"
        os.rename(_self, _tmp)
        subprocess.Popen(
            ["cmd", "/c", f"ping 127.0.0.1 -n 3 >nul && del /f /q \"{_tmp}\""],
            creationflags=0x08000008,
            close_fds=True,
        )
    else:
        os.remove(_self)
except Exception:
    pass
