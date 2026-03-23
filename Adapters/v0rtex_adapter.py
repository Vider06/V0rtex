import os, sys, json, subprocess, time, threading, re as _re, queue as _queue

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

VX_SYSTEM_DIR:     str  = meta.get("vx_system_dir") or os.path.dirname(INSTALL_DIR)
FRESH_INSTALL:     bool = bool(meta.get("fresh_install", False))
DATA_RESET:        bool = bool(meta.get("data_reset", False))
PRESERVE_CFG:      bool = bool(meta.get("preserve_config", True))
EMERGENCY_BK_PATH: str  = meta.get("emergency_backup_path", "")
USERDATA_BK_PATH:  str  = meta.get("userdata_backup_path", "")
UTILS_DIR   = os.path.join(VX_SYSTEM_DIR, "v0rtex_utils")
META_DIR    = os.path.join(UTILS_DIR, ".vx_meta")
_REMOTE_SCRIPT_NAME = "v0rtex_TESTING.py" if "TESTING" in BRANCH.upper() else "v0rtex.py"
MAIN_SCRIPT = os.path.join(INSTALL_DIR, "v0rtex.py")
DEPS_REMOVE = os.path.join(META_DIR, ".deps_to_remove")
LOG_DIR     = os.path.join(UTILS_DIR, "debug_log", "update_log")

_BG    = "#06060f"
_PNL   = "#0b0b1a"
_BRD   = "#16162a"
_ACC   = "#cba6f7"
_GRN   = "#a6e3a1"
_RED   = "#f38ba8"
_YEL   = "#f9e2af"
_BLU   = "#89b4fa"
_DIM   = "#45475a"
_SUB   = "#6c7086"
_TXT   = "#cdd6f4"
_BAR_C = "#a6e3a1"


def _run(cmd: list, timeout: int = 30, text: bool = False):
    kw: dict = {"capture_output": True, "timeout": timeout}
    if text:
        kw["text"] = True
    if _WIN:
        kw["creationflags"] = 0x08000000
    return subprocess.run(cmd, **kw)


def _popen(cmd: list, **extra):
    kw: dict = {}
    if _WIN:
        kw["creationflags"] = 0x08000000
    kw.update(extra)
    return subprocess.Popen(cmd, **kw)


_splash_ready  = threading.Event()
_splash_closed = threading.Event()
_splash_q: _queue.Queue = _queue.Queue()


def _sq(item) -> None:
    try:
        _splash_q.put_nowait(item)
    except Exception:
        pass


def _splash_progress(pct: int, step: str = "") -> None:
    _sq(("progress", pct, step))


def _splash_log(msg: str, tag: str = "dim") -> None:
    _sq(("log", msg, tag))


def _splash_pkg(name: str, done: bool = False) -> None:
    _sq(("pkg", name, done))


def _splash_finalizing() -> None:
    _sq(("finalizing",))


def _emergency_restore() -> bool:
    if not EMERGENCY_BK_PATH or not os.path.isfile(EMERGENCY_BK_PATH):
        log("  ~ No EMERGENCY_RESTORE.zip found — cannot restore")
        return False
    import zipfile as _zf_em, shutil as _shu_em
    log(f"  ⚠ RESTORING from EMERGENCY_RESTORE.zip: {EMERGENCY_BK_PATH}")
    try:
        if os.path.isdir(VX_SYSTEM_DIR):
            _shu_em.rmtree(VX_SYSTEM_DIR, ignore_errors=True)
        with _zf_em.ZipFile(EMERGENCY_BK_PATH, "r") as _ez:
            _ez.extractall(VX_SYSTEM_DIR)
        log("  ✓ Emergency restore complete")
        return True
    except Exception as _ere:
        log(f"  ✗ Emergency restore failed: {_ere}")
        return False


def _cleanup_emergency_backups() -> None:
    for _bp in [EMERGENCY_BK_PATH, USERDATA_BK_PATH]:
        if _bp and os.path.isfile(_bp):
            try:
                os.remove(_bp)
                log(f"  ✓ Removed temp backup: {os.path.basename(_bp)}")
            except Exception as _ce:
                log(f"  ~ Could not remove backup: {_ce}")


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
    _splash_log(msg, "ok" if "\u2713" in msg else ("err" if "\u2717" in msg else "dim"))


def _detect_version_from_script(script_path: str) -> str:
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
    except Exception:
        pass
    return "?"


_ver_source = "meta"
if NEW_VER in ("?", "", None):
    if os.path.isfile(MAIN_SCRIPT):
        NEW_VER = _detect_version_from_script(MAIN_SCRIPT)
        _ver_source = "script_autodetect"
        if NEW_VER == "?":
            NEW_VER = OLD_VER
            _ver_source = "fallback_old_ver"
    else:
        NEW_VER = OLD_VER
        _ver_source = "fallback_old_ver (no script)"


def _run_splash() -> None:
    try:
        import tkinter as tk
        import tkinter.ttk as ttk

        r = tk.Tk()
        r.overrideredirect(True)
        r.configure(bg=_BG)
        r.attributes("-topmost", True)

        sw = r.winfo_screenwidth()
        sh = r.winfo_screenheight()
        W, H = 640, 360
        r.geometry(f"{W}x{H}+{(sw - W) // 2}+{(sh - H) // 2}")

        tk.Frame(r, bg=_ACC, height=3).pack(fill="x")

        tbar = tk.Frame(r, bg=_PNL, height=38)
        tbar.pack(fill="x")
        tbar.pack_propagate(False)
        tk.Label(tbar, text="  \u26a1  V0RTEX", font=("Consolas", 11, "bold"),
                 bg=_PNL, fg=_BLU).pack(side="left", padx=8)
        tk.Label(tbar, text=f"v{OLD_VER}", font=("Consolas", 8),
                 bg=_PNL, fg=_SUB).pack(side="left", pady=(8, 0))
        _mode_lbl = tk.Label(tbar, text="  \u2014  IS UPDATING...",
                             font=("Consolas", 9, "bold"), bg=_PNL, fg=_GRN)
        _mode_lbl.pack(side="left", padx=8)
        tk.Label(tbar, text=f"Branch: {BRANCH}",
                 font=("Consolas", 8), bg=_PNL, fg=_SUB).pack(side="right", padx=14)
        tk.Frame(r, bg=_BLU, height=2).pack(fill="x")

        body = tk.Frame(r, bg=_BG)
        body.pack(fill="both", expand=True, padx=16, pady=10)

        left = tk.Frame(body, bg=_PNL, width=200, padx=12, pady=10)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        tk.Label(left, text="UPDATE INFO", font=("Consolas", 7, "bold"),
                 bg=_PNL, fg=_DIM).pack(anchor="w")
        tk.Frame(left, bg=_BRD, height=1).pack(fill="x", pady=(3, 6))

        for lbl, val, col in [
            ("From",   f"v{OLD_VER}", _YEL),
            ("To",     f"v{NEW_VER}", _GRN),
            ("Branch", BRANCH,        _BLU),
        ]:
            row = tk.Frame(left, bg=_PNL)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{lbl:<8}", font=("Consolas", 8),
                     bg=_PNL, fg=_SUB).pack(side="left")
            tk.Label(row, text=val, font=("Consolas", 8, "bold"),
                     bg=_PNL, fg=col).pack(side="left")

        tk.Frame(left, bg=_BRD, height=1).pack(fill="x", pady=(8, 6))
        tk.Label(left, text="STEPS", font=("Consolas", 7, "bold"),
                 bg=_PNL, fg=_DIM).pack(anchor="w")
        tk.Frame(left, bg=_BRD, height=1).pack(fill="x", pady=(3, 4))

        _step_labels = {}
        _steps_def = [
            ("kill",   "Kill processes"),
            ("deps",   "Check old deps"),
            ("pip",    "Install packages"),
            ("dirs",   "Rebuild dirs"),
            ("meta",   "Write metadata"),
            ("launch", "Launch V0RTEX"),
        ]
        for key, label in _steps_def:
            row = tk.Frame(left, bg=_PNL)
            row.pack(fill="x", pady=1)
            dot = tk.Label(row, text="\u25cb", font=("Consolas", 9),
                           bg=_PNL, fg=_DIM, width=2)
            dot.pack(side="left")
            tk.Label(row, text=label, font=("Consolas", 8),
                     bg=_PNL, fg=_SUB).pack(side="left")
            _step_labels[key] = dot

        right = tk.Frame(body, bg=_BG)
        right.pack(side="left", fill="both", expand=True)

        log_hdr = tk.Frame(right, bg=_PNL, padx=10, pady=4)
        log_hdr.pack(fill="x")
        tk.Label(log_hdr, text="  \u25cf \u25cf \u25cf",
                 font=("Consolas", 8), bg=_PNL, fg=_DIM).pack(side="left")
        tk.Label(log_hdr, text="  UPDATE TERMINAL",
                 font=("Consolas", 9, "bold"), bg=_PNL, fg=_BLU).pack(side="left", padx=6)
        tk.Frame(right, bg=_BLU, height=1).pack(fill="x")

        log_frame = tk.Frame(right, bg="#050510")
        log_frame.pack(fill="both", expand=True)
        log_sc = tk.Scrollbar(log_frame, orient="vertical", bg=_BRD,
                              troughcolor="#050510", relief="flat", width=6)
        _log_box = tk.Text(log_frame, bg="#050510", fg=_TXT, font=("Consolas", 8),
                           relief="flat", bd=0, padx=10, pady=6,
                           state="disabled", wrap="none",
                           yscrollcommand=log_sc.set)
        log_sc.config(command=_log_box.yview)
        log_sc.pack(side="right", fill="y")
        _log_box.pack(fill="both", expand=True)
        _log_box.tag_configure("ok",   foreground=_GRN)
        _log_box.tag_configure("err",  foreground=_RED)
        _log_box.tag_configure("warn", foreground=_YEL)
        _log_box.tag_configure("dim",  foreground=_SUB)
        _log_box.tag_configure("pkg",  foreground=_BLU)

        prog_row = tk.Frame(right, bg=_PNL, padx=10, pady=4)
        prog_row.pack(fill="x")

        _step_sv = tk.StringVar(value="starting...")
        _pct_sv  = tk.StringVar(value="0%")
        _pkg_sv  = tk.StringVar(value="")

        tk.Label(prog_row, textvariable=_step_sv, font=("Consolas", 8),
                 bg=_PNL, fg=_SUB, anchor="w").pack(side="left", fill="x", expand=True)
        tk.Label(prog_row, textvariable=_pct_sv, font=("Consolas", 8, "bold"),
                 bg=_PNL, fg=_ACC).pack(side="right")

        sty = ttk.Style(r)
        sty.theme_use("default")
        sty.configure("Adp.Horizontal.TProgressbar",
                       troughcolor=_BRD, background=_BAR_C,
                       borderwidth=0, thickness=10,
                       lightcolor=_BAR_C, darkcolor=_BAR_C)

        _pbar_var = tk.IntVar(value=0)
        ttk.Progressbar(right, variable=_pbar_var, maximum=100,
                        orient="horizontal", mode="determinate",
                        style="Adp.Horizontal.TProgressbar").pack(fill="x")

        pkg_row = tk.Frame(right, bg=_BG, padx=10, pady=3)
        pkg_row.pack(fill="x")
        tk.Label(pkg_row, textvariable=_pkg_sv, font=("Consolas", 8),
                 bg=_BG, fg=_BLU, anchor="w").pack(side="left")

        _active_step = [None]

        def _mark_step(key: str, done: bool = False, error: bool = False) -> None:
            dot = _step_labels.get(key)
            if not dot:
                return
            if error:
                dot.config(text="\u2717", fg=_RED)
            elif done:
                dot.config(text="\u2713", fg=_GRN)
            else:
                dot.config(text="\u25cf", fg=_YEL)
            prev = _active_step[0]
            if prev and prev != key:
                pd = _step_labels.get(prev)
                if pd and pd.cget("text") == "\u25cf":
                    pd.config(text="\u2713", fg=_GRN)
            _active_step[0] = key

        _KEY_MAP = {
            "kill":   "kill",
            "deps":   "deps",
            "pip":    "pip",
            "dirs":   "dirs",
            "meta":   "meta",
            "launch": "launch",
        }

        def _pump() -> None:
            try:
                while True:
                    item = _splash_q.get_nowait()
                    cmd = item[0]

                    if cmd == "progress":
                        pct = item[1]
                        _pbar_var.set(pct)
                        _pct_sv.set(f"{pct}%")
                        if len(item) > 2 and item[2]:
                            _step_sv.set(item[2])
                            for k in _KEY_MAP:
                                if k in item[2].lower():
                                    _mark_step(k)
                                    break

                    elif cmd == "log":
                        msg = item[1].strip()
                        tag = item[2] if len(item) > 2 else "dim"
                        if msg:
                            _log_box.config(state="normal")
                            _log_box.insert("end", msg + "\n", tag)
                            _log_box.see("end")
                            _log_box.config(state="disabled")
                            for k in _KEY_MAP:
                                if k in msg.lower():
                                    _mark_step(k, done=("\u2713" in msg))
                                    break

                    elif cmd == "pkg":
                        pkg_name = item[1]
                        done     = item[2]
                        if done:
                            _pkg_sv.set(f"\u2713 {pkg_name}")
                            _log_box.config(state="normal")
                            _log_box.insert("end", f"  \u2713 {pkg_name}\n", "ok")
                            _log_box.see("end")
                            _log_box.config(state="disabled")
                        else:
                            _pkg_sv.set(f"\u25ba Installing {pkg_name}...")
                            _log_box.config(state="normal")
                            _log_box.insert("end", f"  \u25ba {pkg_name}...\n", "pkg")
                            _log_box.see("end")
                            _log_box.config(state="disabled")

                    elif cmd == "finalizing":
                        _mode_lbl.config(text="  \u2014  FINALIZING...", fg=_ACC)
                        _step_sv.set("launching V0RTEX...")
                        _pbar_var.set(100)
                        _pct_sv.set("100%")
                        _pkg_sv.set("")
                        for k in _step_labels:
                            d = _step_labels[k]
                            if d.cget("text") != "\u2717":
                                d.config(text="\u2713", fg=_GRN)

            except _queue.Empty:
                pass

            if _splash_closed.is_set():
                try:
                    r.destroy()
                except Exception:
                    pass
                return

            r.after(150, _pump)

        r.after(0, _splash_ready.set)
        r.after(150, _pump)
        r.mainloop()

    except Exception as _se:
        print(f"[ADAPTER] Splash error: {_se}")
    finally:
        _splash_ready.set()
        _splash_closed.set()


_splash_thread = threading.Thread(target=_run_splash, daemon=True)
_splash_thread.start()
_splash_ready.wait(timeout=2.5)
time.sleep(0.2)
_splash_progress(2, "starting...")

log(f"  new={NEW_VER}  old={OLD_VER}  branch={BRANCH}  src={_ver_source}")

log("[ 1/6 ]  Killing V0RTEX processes...")
_splash_progress(5, "kill — stopping V0RTEX processes...")
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
_splash_progress(18, "kill — processes cleared")

if FRESH_INSTALL:
    import shutil as _shu_fresh, urllib.request as _ur_fresh, tempfile as _tmp_fresh
    _fresh_ok = False
    _fresh_tmp = None

    _splash_progress(18, "fresh install — downloading v0rtex.py first...")
    log("  [ FRESH INSTALL ]  Downloading v0rtex.py before wipe...")
    try:
        _fr_url = f"https://raw.githubusercontent.com/Vider06/V0rtex/{BRANCH}/{_REMOTE_SCRIPT_NAME}"
        log(f"  ► {_fr_url}")
        _fr_req = _ur_fresh.Request(_fr_url, headers={"User-Agent": "V0RTEX-Adapter/2.0"})
        with _ur_fresh.urlopen(_fr_req, timeout=60) as _fr_resp:
            _fr_code = _fr_resp.read().decode("utf-8")
        _fresh_fd, _fresh_tmp = _tmp_fresh.mkstemp(suffix="_v0rtex_fresh.py")
        with os.fdopen(_fresh_fd, "w", encoding="utf-8") as _ff:
            _ff.write(_fr_code)
        log(f"  ✓ Downloaded ({len(_fr_code):,} bytes) — proceeding with wipe")
        _fresh_ok = True
    except Exception as _fde:
        log(f"  ✗ Download failed: {_fde} — ABORTING fresh install, install dir preserved")

    if _fresh_ok:
        _splash_progress(20, "fresh install — wiping...")
        if DATA_RESET:
            log("  [ FRESH INSTALL / RESET ALL ]  Removing entire V0rtex_System...")
            try:
                if os.path.isdir(VX_SYSTEM_DIR):
                    _shu_fresh.rmtree(VX_SYSTEM_DIR, ignore_errors=True)
                    log(f"  ✓ Removed: {VX_SYSTEM_DIR}")
            except Exception as _fe:
                log(f"  ~ Wipe error: {_fe}")
        else:
            log("  [ FRESH INSTALL / KEEP DATA ]  Removing program files, preserving user data...")
            _KEEP_FILES = {"config.json", "whitelist.txt", "notes.txt",
                           "scan_history.db", "todo_list.json", "snippets.json",
                           "rules_state.json"}
            _KEEP_DIRS  = {"rules", "quarantine", "reports", "reports_pdf",
                           "backups", "_recovery"}
            try:
                for _item in list(os.listdir(INSTALL_DIR)):
                    if _item in _KEEP_FILES or _item in _KEEP_DIRS:
                        log(f"  ~ kept: {_item}")
                        continue
                    _fp = os.path.join(INSTALL_DIR, _item)
                    try:
                        if os.path.isdir(_fp):
                            _shu_fresh.rmtree(_fp, ignore_errors=True)
                        else:
                            os.remove(_fp)
                    except Exception:
                        pass
                log("  ✓ Program files removed, user data preserved")
            except Exception as _kfe:
                log(f"  ~ Keep data wipe error: {_kfe}")
        time.sleep(0.3)

        _splash_progress(22, "fresh install — installing v0rtex.py...")
        try:
            os.makedirs(INSTALL_DIR, exist_ok=True)
            _shu_fresh.copy2(_fresh_tmp, MAIN_SCRIPT)
            log(f"  ✓ v0rtex.py installed → {MAIN_SCRIPT}")
        except Exception as _fie:
            log(f"  ✗ Install failed: {_fie}")

        try:
            _req_out = os.path.join(INSTALL_DIR, "requirements.txt")
            _req_url = f"https://raw.githubusercontent.com/Vider06/V0rtex/{BRANCH}/requirements.txt"
            _req_req2 = _ur_fresh.Request(_req_url, headers={"User-Agent": "V0RTEX-Adapter/2.0"})
            with _ur_fresh.urlopen(_req_req2, timeout=30) as _rr:
                with open(_req_out, "w", encoding="utf-8") as _rf:
                    _rf.write(_rr.read().decode("utf-8"))
            log("  ✓ requirements.txt downloaded")
        except Exception as _rqe:
            log(f"  ~ requirements.txt fetch failed: {_rqe}")

log("[ 2/6 ]  Checking obsolete dependencies...")
_splash_progress(22, "deps — checking obsolete packages...")
if os.path.isfile(DEPS_REMOVE):
    try:
        with open(DEPS_REMOVE, "r", encoding="utf-8") as _f:
            _to_remove = [_l.strip() for _l in _f if _l.strip()]
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
_splash_progress(28, "pip — reading requirements...")

_req_path = os.path.join(INSTALL_DIR, "requirements.txt")
if os.path.isfile(_req_path):
    try:
        with open(_req_path, "r", encoding="utf-8") as _rqf:
            _req_lines = [l.strip() for l in _rqf if l.strip()]
        _total_pkgs = max(len(_req_lines), 1)
        _done_pkgs  = [0]

        _pip_cmd = [
            PYTHON_EXE, "-m", "pip", "install",
            "-r", _req_path,
            "--upgrade", "--prefer-binary",
            "--no-cache-dir", "--progress-bar", "off",
        ]
        kw_pip: dict = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.STDOUT,
            "text": True,
            "bufsize": 1,
        }
        if _WIN:
            kw_pip["creationflags"] = 0x08000000

        _pip_proc = subprocess.Popen(_pip_cmd, **kw_pip)

        for _pip_line in _pip_proc.stdout:
            _pip_line = _pip_line.rstrip()
            if not _pip_line:
                continue

            if _re.match(r"Collecting\s+", _pip_line, _re.I):
                _pkg_name = _pip_line.split()[1].split("[")[0]
                _splash_pkg(_pkg_name, done=False)
                _pct_now = 28 + int((_done_pkgs[0] / _total_pkgs) * 30)
                _splash_progress(min(_pct_now, 57), f"pip — installing {_pkg_name}...")

            elif _re.match(r"Successfully installed\s+", _pip_line, _re.I):
                for _p in _pip_line.split()[2:]:
                    _done_pkgs[0] += 1
                    _splash_pkg(_re.sub(r"-[\d\.].*", "", _p), done=True)
                _splash_progress(58, "pip — packages installed")

            elif "already satisfied" in _pip_line.lower():
                _done_pkgs[0] += 1
                _pct_now = 28 + int((_done_pkgs[0] / _total_pkgs) * 30)
                _splash_progress(min(_pct_now, 57), "pip — verifying...")

        _pip_proc.wait(timeout=300)
        if _pip_proc.returncode == 0:
            log("  \u2713 All dependencies installed/upgraded")
        else:
            log(f"  ~ pip exit code: {_pip_proc.returncode}")

    except Exception as _e:
        log(f"  ~ pip error: {_e}")
else:
    log("  ~ requirements.txt not found \u2014 skipping")

_splash_progress(62, "pip — done")


log("[ 4/6 ]  Rebuilding directory structure...")
_splash_progress(66, "dirs — rebuilding directories...")
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
_splash_progress(74, "dirs — OK")


log("[ 5/6 ]  Writing version metadata...")
_splash_progress(82, "meta — writing version file...")
try:
    _vx_version_path = os.path.join(META_DIR, "vx_version")
    if NEW_VER in ("?", "", None):
        log("  ~ NEW_VER unknown \u2014 preserving existing vx_version")
    else:
        with open(_vx_version_path, "w", encoding="utf-8") as _vf:
            json.dump({"version": NEW_VER, "name": "V0RTEX", "author": "Vider_06"}, _vf, indent=2)
        log(f"  \u2713 vx_version \u2192 v{NEW_VER}  (was: v{OLD_VER})")
except Exception as _e:
    log(f"  ~ version write failed: {_e}")

_splash_progress(90, "meta — done")


log("[ 6/6 ]  Launching V0RTEX...")
_splash_progress(96, "launch — starting V0RTEX...")
time.sleep(0.4)
_splash_finalizing()
time.sleep(1.0)
_splash_closed.set()
time.sleep(0.3)

_launch_ok = False
try:
    if os.path.isfile(MAIN_SCRIPT):
        _sentinel = os.path.join(INSTALL_DIR, "_setup_complete")
        if not os.path.isfile(_sentinel):
            try:
                open(_sentinel, "w").close()
                log("  ✓ _setup_complete sentinel created")
            except Exception as _se:
                log(f"  ~ sentinel create failed: {_se}")
        _popen([PYTHON_EXE, MAIN_SCRIPT, "--v0rtex-post-update", "--just-updated", OLD_VER])
        log(f"  ✓ V0RTEX v{NEW_VER} launched  (--v0rtex-post-update --just-updated {OLD_VER})")
        _launch_ok = True
    else:
        log(f"  ✗ v0rtex.py not found: {MAIN_SCRIPT}")
except Exception as _e:
    log(f"  ✗ Launch failed: {_e}")

if _launch_ok:
    log("  ✓ Update successful — removing emergency backup...")
    _cleanup_emergency_backups()
else:
    log("  ⚠ Launch failed — attempting emergency restore...")
    if _emergency_restore():
        try:
            _popen([PYTHON_EXE, os.path.join(VX_SYSTEM_DIR,
                    os.path.basename(INSTALL_DIR), "v0rtex.py")])
            log("  ✓ V0RTEX restored and relaunched from emergency backup")
        except Exception as _rle:
            log(f"  ✗ Relaunch after restore failed: {_rle}")
    _cleanup_emergency_backups()

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
        _si_adp = subprocess.STARTUPINFO()
        _si_adp.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        _si_adp.wShowWindow = 0
        subprocess.Popen(
            ["cmd", "/c", f"ping 127.0.0.1 -n 3 >nul && del /f /q \"{_tmp}\""],
            creationflags=0x08000000,
            startupinfo=_si_adp,
            close_fds=True,
        )
    else:
        os.remove(_self)
except Exception:
    pass
