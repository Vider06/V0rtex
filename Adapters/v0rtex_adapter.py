import os, sys, json, subprocess, time, threading, tempfile, urllib.request, shutil

_WIN = sys.platform == "win32"
BRANCH      = "Windows_Release"
GITHUB_BASE = "https://raw.githubusercontent.com/Vider06/V0rtex"

META_PATH     = sys.argv[1] if len(sys.argv) > 1 else None
_settings: dict = {}
if META_PATH and os.path.isfile(META_PATH):
    try:
        with open(META_PATH, "r", encoding="utf-8") as _f:
            _settings = json.load(_f)
    except Exception as _e:
        print(f"[ADAPTER] Cannot read settings: {_e}")

INSTALL_DIR = _settings.get("install_dir") or os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE  = _settings.get("python_exe")  or sys.executable
OLD_VER     = _settings.get("old_version",  "?")
BRANCH      = _settings.get("branch", BRANCH)
V0RTEX_PIDS = _settings.get("v0rtex_pids", [])
BACKUP_PATH = _settings.get("backup_path", "")
RESTART_LVL = _settings.get("restart_level", "user")

UTILS_DIR   = os.path.join(os.path.dirname(INSTALL_DIR), "v0rtex_utils")
META_DIR    = os.path.join(UTILS_DIR, ".vx_meta")
LOG_DIR     = _settings.get("log_dir") or os.path.join(UTILS_DIR, "debug_log", "update_log")
COMPAT_URL  = f"{GITHUB_BASE}/{BRANCH}/compat_map.json"
MAIN_SCRIPT = os.path.join(INSTALL_DIR, "v0rtex.py")
MAX_DIRECT_HOPS = 5


def _run(cmd, timeout=30, text=False):
    kw = {"capture_output": True, "timeout": timeout}
    if text: kw["text"] = True
    if _WIN: kw["creationflags"] = 0x08000000
    return subprocess.run(cmd, **kw)

def _popen(cmd, **kw):
    if _WIN: kw.setdefault("creationflags", 0x08000000)
    return subprocess.Popen(cmd, **kw)

def log(msg: str, tag: str = "INFO") -> None:
    ts   = time.strftime("%H:%M:%S")
    line = f"[{ts}] [{tag:<5}] {msg}"
    print(line)
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, f"adapter_{time.strftime('%Y%m%d')}.log"), "a", encoding="utf-8") as lf:
            lf.write(line + "\n")
    except Exception:
        pass

def _save_settings():
    if META_PATH:
        try:
            with open(META_PATH, "w", encoding="utf-8") as sf:
                json.dump(_settings, sf, indent=2)
        except Exception as e:
            log(f"  ~ settings save: {e}", "WARN")

def _fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "V0RTEX-Adapter/2.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")

def _parse_ver(v: str) -> tuple:
    v = str(v).strip().lstrip("v")
    parts = []
    for p in v.split("."):
        p = p.upper().replace("X", "")
        if p.isdigit(): parts.append(int(p))
    while len(parts) < 4: parts.append(0)
    return tuple(parts[:4])


_settings["adapter_pid"] = os.getpid()
_save_settings()

log(f"Adapter started  PID={os.getpid()}  old={OLD_VER}  branch={BRANCH}", "BOOT")
log(f"install_dir = {INSTALL_DIR}", "BOOT")


_splash_ready  = threading.Event()
_splash_closed = threading.Event()
_splash_status = [None]
_splash_root   = [None]

def _run_splash():
    try:
        import tkinter as tk
        r = tk.Tk()
        r.overrideredirect(True)
        r.configure(bg="#0d0d14")
        r.attributes("-topmost", True)
        sw, sh = r.winfo_screenwidth(), r.winfo_screenheight()
        W, H = 520, 180
        r.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")
        tk.Frame(r, bg="#cba6f7", height=3).pack(fill="x")
        tk.Label(r, text="V 0 R T E X", font=("Consolas",22,"bold"), bg="#0d0d14", fg="#cba6f7").pack(pady=(16,2))
        lbl = tk.Label(r, text="⚡  IS UPDATING...  ⚡", font=("Consolas",12,"bold"), bg="#0d0d14", fg="#a6e3a1")
        lbl.pack()
        tk.Label(r, text=f"v{OLD_VER}  →  latest  ·  {BRANCH}", font=("Consolas",9), bg="#0d0d14", fg="#585b70").pack(pady=2)
        sv = tk.StringVar(value="Initialising...")
        _splash_status[0] = sv
        tk.Label(r, textvariable=sv, font=("Consolas",8), bg="#0d0d14", fg="#45475a").pack(pady=(4,0))
        _splash_root[0] = r
        _frames = ["⚡  IS UPDATING...  ⚡", "✦  IS UPDATING...  ✦", "◈  IS UPDATING...  ◈"]
        _fi = [0]
        def _tick():
            if _splash_closed.is_set():
                try: r.destroy()
                except Exception: pass
                return
            _fi[0] = (_fi[0]+1) % len(_frames)
            try: lbl.config(text=_frames[_fi[0]])
            except Exception: pass
            r.after(500, _tick)
        r.after(0, _splash_ready.set)
        r.after(500, _tick)
        r.mainloop()
    except Exception as se:
        log(f"  ~ splash error: {se}", "WARN")
    finally:
        _splash_ready.set()
        _splash_closed.set()

def _splash_set(msg: str):
    try:
        if _splash_status[0] and _splash_root[0]:
            _splash_root[0].after(0, lambda m=msg: _splash_status[0].set(m))
    except Exception:
        pass

threading.Thread(target=_run_splash, daemon=True).start()
_splash_ready.wait(timeout=2.0)
time.sleep(0.15)


log("[ 1/5 ]  Killing V0RTEX processes...", "STEP")
_splash_set("Stopping V0RTEX...")
_SCRIPTS = ["v0rtex.py","v0rtex_reinstall.py","v0rtex_uninstall.py","v0rtex_updater.py","v0rtex_recovery_ui.py"]
_killed  = 0

if V0RTEX_PIDS:
    for _pid in V0RTEX_PIDS:
        if _pid == os.getpid(): continue
        try:
            if _WIN:
                import ctypes as _ct
                _h = _ct.windll.kernel32.OpenProcess(0x0001|0x1000, False, _pid)
                if _h:
                    _ct.windll.kernel32.TerminateProcess(_h, 0)
                    _ct.windll.kernel32.CloseHandle(_h)
                    _killed += 1
                    log(f"  ✓ PID {_pid} killed", "OK")
                else:
                    log(f"  · PID {_pid} already gone", "INFO")
            else:
                os.kill(_pid, 9); _killed += 1
                log(f"  ✓ PID {_pid} killed", "OK")
        except Exception as _ke:
            log(f"  ~ PID {_pid}: {_ke}", "WARN")
    time.sleep(0.8)

try:
    import psutil as _psu
    for _proc in _psu.process_iter(["pid","name","cmdline"]):
        try:
            _cmd = " ".join(_proc.info.get("cmdline") or [])
            if any(_s in _cmd for _s in _SCRIPTS) and _proc.pid != os.getpid():
                _proc.kill(); _killed += 1
                log(f"  ✓ straggler PID {_proc.pid} killed", "OK")
        except Exception:
            pass
    log(f"  ✓ psutil sweep done — total killed: {_killed}", "OK")
except ImportError:
    log("  ~ psutil unavailable", "WARN")
    if not V0RTEX_PIDS and _WIN:
        try:
            _r = _run(["tasklist","/FI","IMAGENAME eq python.exe","/FI","IMAGENAME eq pythonw.exe","/FO","CSV","/NH"], timeout=10, text=True)
            for _line in _r.stdout.splitlines():
                _parts = _line.strip().strip('"').split('","')
                if len(_parts) < 2: continue
                try: _pid = int(_parts[1])
                except ValueError: continue
                if _pid == os.getpid(): continue
                _wm = _run(["wmic","process","where",f"ProcessId={_pid}","get","CommandLine","/format:list"], timeout=5, text=True)
                if any(_s.lower() in _wm.stdout.lower() for _s in _SCRIPTS):
                    _run(["taskkill","/F","/PID",str(_pid)], timeout=5)
                    _killed += 1
        except Exception as _we:
            log(f"  ~ tasklist fallback: {_we}", "WARN")

time.sleep(0.8)
log(f"  → total killed: {_killed}", "INFO")


log("[ 2/5 ]  Fetching compat_map.json...", "STEP")
_splash_set("Checking version compatibility...")
_compat: dict = {}
try:
    _compat = json.loads(_fetch(COMPAT_URL, timeout=15))
    _chain_all = _compat.get("chain", [])
    log(f"  ✓ compat_map loaded — {len(_chain_all)} entries  latest={_compat.get('latest_version','?')}", "OK")
except Exception as _ce:
    log(f"  ✗ compat_map fetch failed: {_ce}", "ERR")
    _compat = {}


log("[ 3/5 ]  Analysing update path...", "STEP")
_splash_set("Planning update path...")
_cur_t          = _parse_ver(OLD_VER)
_latest_ver     = _compat.get("latest_version", "")
_chain          = _compat.get("chain", [])
_use_trampoline = False
_cur_idx        = -1

if _chain and _latest_ver:
    for _i, _entry in enumerate(_chain):
        if _parse_ver(_entry["version"]) == _cur_t:
            _cur_idx = _i; break
    if _cur_idx == -1:
        for _i, _entry in enumerate(_chain):
            if _parse_ver(_entry["version"]) <= _cur_t:
                _cur_idx = _i
        _cur_idx = max(_cur_idx, 0)
        log(f"  ~ {OLD_VER} not in chain, mapped to index {_cur_idx}", "WARN")
    _hops = len(_chain) - 1 - _cur_idx
    _max_hops = _compat.get("max_direct_hops", MAX_DIRECT_HOPS)
    log(f"  → position {_cur_idx}/{len(_chain)-1}  hops={_hops}  max={_max_hops}", "INFO")
    if _hops > _max_hops:
        _use_trampoline = True
        log("  → TRAMPOLINE selected", "INFO")
    else:
        log("  → DIRECT selected", "INFO")
else:
    log("  ~ no compat chain — assuming direct", "WARN")


log("[ 4/5 ]  Checking obsolete dependencies...", "STEP")
_DEPS_REMOVE = os.path.join(META_DIR, ".deps_to_remove")
if os.path.isfile(_DEPS_REMOVE):
    try:
        with open(_DEPS_REMOVE, "r", encoding="utf-8") as _f:
            _to_remove = [l.strip() for l in _f if l.strip()]
        for _pkg in _to_remove:
            try:
                _r2 = _run([PYTHON_EXE,"-m","pip","uninstall","-y",_pkg], timeout=60, text=True)
                log(f"  {'✓' if _r2.returncode==0 else '~'} removed {_pkg}", "OK" if _r2.returncode==0 else "WARN")
            except Exception as _e2:
                log(f"  ~ {_pkg}: {_e2}", "WARN")
        os.remove(_DEPS_REMOVE)
    except Exception as _de:
        log(f"  ~ deps_to_remove: {_de}", "WARN")
else:
    log("  ~ no .deps_to_remove", "INFO")


log("[ 5/5 ]  Executing update strategy...", "STEP")


def _do_final_install(latest_code: str, new_ver: str):
    log("  [ FINAL INSTALL ] Starting...", "INFO")
    _splash_set("FINALIZING UPDATE...")

    _REQUIRED_DIRS = [
        INSTALL_DIR,
        os.path.join(INSTALL_DIR,"rules"), os.path.join(INSTALL_DIR,"rules","external"),
        os.path.join(INSTALL_DIR,"quarantine"), os.path.join(INSTALL_DIR,"reports"),
        os.path.join(INSTALL_DIR,"reports_pdf"), os.path.join(INSTALL_DIR,"backups"),
        os.path.join(INSTALL_DIR,"_recovery"), os.path.join(INSTALL_DIR,"sandbox_env"),
        os.path.join(INSTALL_DIR,"sandbox_env","drop"), os.path.join(INSTALL_DIR,"threat_feeds"),
        os.path.join(INSTALL_DIR,"pcap_dumps"), UTILS_DIR, META_DIR,
        os.path.join(UTILS_DIR,"debug_log","crash_log"),
        os.path.join(UTILS_DIR,"debug_log","session_log"),
        os.path.join(UTILS_DIR,"debug_log","trampoline_log"),
        os.path.join(UTILS_DIR,"debug_log","admin_log"),
        os.path.join(UTILS_DIR,"debug_log","update_log"),
        os.path.join(UTILS_DIR,"debug_log","setup_log"),
        os.path.join(UTILS_DIR,"debug_log","recovery_ops"),
        os.path.join(UTILS_DIR,"Crash_Full_Report"),
    ]
    for _d in _REQUIRED_DIRS:
        try: os.makedirs(_d, exist_ok=True)
        except Exception as _de2: log(f"  ~ dir {os.path.basename(_d)}: {_de2}", "WARN")
    log("  ✓ directories OK", "OK")

    _splash_set("Installing V0RTEX...")
    try:
        _tmp_w = MAIN_SCRIPT + ".update_tmp"
        with open(_tmp_w, "w", encoding="utf-8") as _wf: _wf.write(latest_code)
        shutil.move(_tmp_w, MAIN_SCRIPT)
        log(f"  ✓ v0rtex.py installed ({len(latest_code):,} bytes)", "OK")
    except Exception as _ie:
        log(f"  ✗ install failed: {_ie}", "ERR")

    _splash_set("Installing dependencies...")
    _req_path = os.path.join(INSTALL_DIR, "requirements.txt")
    if os.path.isfile(_req_path):
        try:
            _rr = _run([PYTHON_EXE,"-m","pip","install","-r",_req_path,
                        "--upgrade","--prefer-binary","-q","--no-cache-dir","--progress-bar","off"],
                       timeout=360, text=True)
            log(f"  {'✓' if _rr.returncode==0 else '~'} pip done (rc={_rr.returncode})",
                "OK" if _rr.returncode==0 else "WARN")
        except Exception as _pe:
            log(f"  ~ pip: {_pe}", "WARN")
    else:
        log("  ~ no requirements.txt", "WARN")

    _splash_set("Restoring user data...")
    _preserve = _settings.get("preserve_config", True)
    _data_reset = _settings.get("data_reset", False)
    _bk = _settings.get("backup_path", "")
    if _bk and os.path.isfile(_bk) and _preserve and not _data_reset:
        try:
            import zipfile as _zf
            with _zf.ZipFile(_bk, "r") as _zr:
                _names = _zr.namelist()
                for _fn in ["config.json","whitelist.txt","notes.txt","todo_list.json",
                            "snippets.json","rules_state.json"]:
                    if _fn in _names:
                        try: _zr.extract(_fn, INSTALL_DIR); log(f"  ✓ restored {_fn}", "OK")
                        except Exception as _re: log(f"  ~ {_fn}: {_re}", "WARN")
                for _db in ["scan_history.db","scan_results.db"]:
                    if _db in _names:
                        try: _zr.extract(_db, INSTALL_DIR); log(f"  ✓ restored {_db}", "OK")
                        except Exception as _dbe: log(f"  ~ {_db}: {_dbe}", "WARN")
                _rc = sum(1 for _zn in _names if _zn.startswith(("reports/","reports_pdf/")))
                for _zn in _names:
                    if _zn.startswith(("reports/","reports_pdf/")):
                        try: _zr.extract(_zn, INSTALL_DIR)
                        except Exception: pass
                if _rc: log(f"  ✓ restored {_rc} report(s)", "OK")
                if _settings.get("update_rules", True):
                    _yrc = 0
                    for _zn in _names:
                        if _zn.startswith("rules/"):
                            try: _zr.extract(_zn, INSTALL_DIR); _yrc += 1
                            except Exception: pass
                    if _yrc: log(f"  ✓ restored {_yrc} rule(s)", "OK")
            log("  ✓ backup restore complete", "OK")
        except Exception as _ze:
            log(f"  ✗ backup restore: {_ze}", "ERR")
    elif _data_reset:
        log("  ~ data_reset=True — skipping restore", "INFO")
    else:
        log("  ~ no backup or preserve_config=False — skipping restore", "INFO")

    try:
        os.makedirs(META_DIR, exist_ok=True)
        with open(os.path.join(META_DIR,"vx_version"),"w",encoding="utf-8") as _vf:
            json.dump({"version": new_ver, "name": "V0RTEX", "author": "Vider_06"}, _vf, indent=2)
        log(f"  ✓ vx_version → {new_ver}", "OK")
    except Exception as _ve:
        log(f"  ~ vx_version: {_ve}", "WARN")

    _splash_set(f"UPDATE COMPLETED!  RESTARTING AT {RESTART_LVL.upper()} LEVEL...")
    log(f"  → Restarting at level: {RESTART_LVL}", "INFO")
    time.sleep(1.2)

    _need_admin  = (RESTART_LVL == "admin")
    _current_pid = os.getpid()
    _tram_dir    = UTILS_DIR
    os.makedirs(_tram_dir, exist_ok=True)
    _tram_path   = os.path.join(_tram_dir, "_vx_post_update_relaunch.py")
    _tram_log    = os.path.join(UTILS_DIR, "debug_log", "trampoline_log", "_post_update_relaunch.log")

    if _WIN:
        _pyw = PYTHON_EXE.replace("python.exe","pythonw.exe")
        if not os.path.isfile(_pyw): _pyw = PYTHON_EXE
        _tram_code = (
            f"import os,sys,time,subprocess,ctypes\n"
            f"_PID={_current_pid}\n_TARGET=r\"{MAIN_SCRIPT}\"\n_PYTHON=r\"{_pyw}\"\n"
            f"_SELF=r\"{_tram_path}\"\n_TASK=\"V0RTEXPostUpdateRelaunch\"\n"
            f"_LOG=r\"{_tram_log}\"\n_ADMIN={_need_admin}\n"
            "def _log(m):\n"
            " import datetime\n"
            " try:\n"
            "  with open(_LOG,'a',encoding='utf-8') as f: f.write(f'[{datetime.datetime.now().strftime(\"%H:%M:%S\")}] {m}\\n')\n"
            " except: pass\n"
            "_log('post-update trampoline started')\n"
            "k32=ctypes.windll.kernel32\ntime.sleep(0.5)\n"
            "try:\n h=k32.OpenProcess(0x0001|0x1000,False,_PID)\n if h: k32.TerminateProcess(h,0);k32.CloseHandle(h);_log('killed')\n else: _log('already gone')\nexcept Exception as e: _log(f'kill err: {e}')\n"
            "for _ in range(30):\n h2=k32.OpenProcess(0x1000,False,_PID)\n if not h2: _log('gone');break\n k32.CloseHandle(h2);time.sleep(0.2)\n"
            "time.sleep(0.4)\n"
            "subprocess.run(['schtasks','/delete','/tn',_TASK,'/f'],capture_output=True)\n"
            "if _ADMIN:\n import ctypes as _c2;_c2.windll.shell32.ShellExecuteW(None,'runas',_PYTHON,f'\"{_TARGET}\"',None,1)\nelse:\n subprocess.Popen([_PYTHON,_TARGET],creationflags=0x08000000)\n"
            "_log('launched')\ntime.sleep(1)\ntry: os.remove(_SELF)\nexcept: pass\n"
        )
        try:
            os.makedirs(os.path.dirname(_tram_log), exist_ok=True)
            with open(_tram_path,"w",encoding="utf-8") as _tf: _tf.write(_tram_code)
            subprocess.run(["schtasks","/delete","/tn","V0RTEXPostUpdateRelaunch","/f"], capture_output=True)
            _ret = subprocess.run([
                "schtasks","/create","/tn","V0RTEXPostUpdateRelaunch",
                "/tr",f'"{_pyw}" "{_tram_path}"',
                "/sc","ONCE","/st","00:00","/f","/RL","LIMITED"
            ], capture_output=True, text=True)
            if _ret.returncode == 0:
                subprocess.run(["schtasks","/run","/tn","V0RTEXPostUpdateRelaunch"], capture_output=True)
                log("  ✓ post-update trampoline triggered (drops admin, relaunches)", "OK")
            else:
                raise RuntimeError(_ret.stderr.strip() or _ret.stdout.strip())
        except Exception as _ste:
            log(f"  ✗ schtasks failed: {_ste} — direct launch fallback", "WARN")
            _popen([PYTHON_EXE, MAIN_SCRIPT])
    else:
        _real_user = os.environ.get("SUDO_USER","")
        _tram_code = (
            f"import os,sys,time,subprocess,signal\n"
            f"_PID={_current_pid}\n_TARGET=r\"{MAIN_SCRIPT}\"\n_PYTHON=r\"{PYTHON_EXE}\"\n"
            f"_SELF=r\"{_tram_path}\"\n_REAL_USER=\"{_real_user}\"\n_ADMIN={_need_admin}\n"
            "time.sleep(0.4)\ntry: os.kill(_PID,signal.SIGTERM)\nexcept: pass\n"
            "for _ in range(25):\n try: os.kill(_PID,0)\n except OSError: break\n time.sleep(0.2)\n"
            "else:\n try: os.kill(_PID,signal.SIGKILL)\n except: pass\n"
            "time.sleep(0.3)\n"
            "if _ADMIN: subprocess.Popen(['sudo',_PYTHON,_TARGET])\n"
            "elif _REAL_USER and os.geteuid()==0: subprocess.Popen(['sudo','-u',_REAL_USER,_PYTHON,_TARGET])\n"
            "else: subprocess.Popen([_PYTHON,_TARGET])\n"
            "time.sleep(1)\ntry: os.remove(_SELF)\nexcept: pass\n"
        )
        try:
            with open(_tram_path,"w",encoding="utf-8") as _tf: _tf.write(_tram_code)
            subprocess.Popen([PYTHON_EXE,_tram_path], start_new_session=True, close_fds=True)
            log("  ✓ unix trampoline launched", "OK")
        except Exception as _ule:
            log(f"  ✗ unix trampoline: {_ule}", "WARN")
            _popen([PYTHON_EXE, MAIN_SCRIPT])


if _use_trampoline:
    log("  [ TRAMPOLINE ] Finding first hop...", "INFO")
    _splash_set("TRAMPOLINE — downloading intermediate version...")
    _next_entry = _chain[_cur_idx+1] if _cur_idx+1 < len(_chain) else None
    if not _next_entry:
        log("  ✗ no next entry — falling back to direct", "ERR")
        _use_trampoline = False
    else:
        _next_ver = _next_entry["version"]
        _next_url = _next_entry.get("raw_url", f"{GITHUB_BASE}/{BRANCH}/v0rtex.py")
        log(f"  → hop target: v{_next_ver}", "INFO")
        _splash_set(f"Downloading v{_next_ver}...")
        try:
            _next_code = _fetch(_next_url, timeout=60)
            import ast as _ast_t; _ast_t.parse(_next_code)
            _tmp_next = os.path.join(tempfile.gettempdir(), f"_v0rtex_tramp_{_next_ver.replace('.','_')}.py")
            with open(_tmp_next,"w",encoding="utf-8") as _nf: _nf.write(_next_code)
            log(f"  ✓ v{_next_ver} downloaded → {_tmp_next}", "OK")
            _bk = _settings.get("backup_path","")
            if _bk and os.path.isfile(_bk):
                _bk2 = os.path.join(tempfile.gettempdir(), os.path.basename(_bk))
                try: shutil.copy2(_bk, _bk2); _settings["backup_path"] = _bk2; log(f"  ✓ backup moved to TEMP", "OK")
                except Exception as _bke: log(f"  ~ backup move: {_bke}", "WARN")
            _settings["trampoline_current_version"] = _next_ver
            _settings["old_version"] = _next_ver
            _save_settings()
            _splash_set("Removing old installation...")
            shutil.rmtree(INSTALL_DIR, ignore_errors=True)
            if not os.path.exists(INSTALL_DIR): log("  ✓ v0rtex_system deleted", "OK")
            elif _WIN: os.system(f'rmdir /s /q "{INSTALL_DIR}"')
            time.sleep(0.4)
            _splash_set(f"Launching v{_next_ver}...")
            _popen([PYTHON_EXE, _tmp_next, "--trampoline-update", META_PATH or ""])
            log(f"  ✓ hop launched — adapter handing off", "OK")
        except Exception as _te:
            log(f"  ✗ trampoline failed: {_te} — falling back to direct", "ERR")
            _use_trampoline = False

if not _use_trampoline:
    log("  [ DIRECT ] Downloading latest v0rtex.py...", "INFO")
    _splash_set("Downloading latest V0RTEX...")
    _latest_url = (_chain[-1].get("raw_url", f"{GITHUB_BASE}/{BRANCH}/v0rtex.py")
                   if _chain else f"{GITHUB_BASE}/{BRANCH}/v0rtex.py")
    log(f"  → {_latest_url}", "INFO")
    _latest_code = None
    try:
        _latest_code = _fetch(_latest_url, timeout=60)
        log(f"  ✓ downloaded ({len(_latest_code):,} bytes)", "OK")
        import ast as _ast_d; _ast_d.parse(_latest_code)
        log("  ✓ syntax verified", "OK")
    except SyntaxError as _se:
        log(f"  ✗ syntax error: {_se}", "ERR"); _latest_code = None
    except Exception as _dle:
        log(f"  ✗ download failed: {_dle}", "ERR")

    if not _latest_code and os.path.isfile(MAIN_SCRIPT):
        log("  ~ using existing v0rtex.py as fallback", "WARN")
        with open(MAIN_SCRIPT,"r",encoding="utf-8") as _ef: _latest_code = _ef.read()

    if _latest_code:
        _do_final_install(_latest_code, _latest_ver or "latest")
    else:
        log("  ✗ no v0rtex.py available — cannot complete update", "ERR")
        _popen([PYTHON_EXE, MAIN_SCRIPT])

_splash_closed.set()
time.sleep(0.5)
log("  → Adapter self-destructing...", "INFO")
try:
    _self = os.path.abspath(__file__)
    if _WIN:
        _d = _self + ".del"
        os.rename(_self, _d)
        subprocess.Popen(["cmd","/c",f"ping 127.0.0.1 -n 3 >nul && del /f /q \"{_d}\""],
                         creationflags=0x08000008, close_fds=True)
    else:
        os.remove(_self)
except Exception:
    pass
log("  ✓ Adapter done.", "OK")
