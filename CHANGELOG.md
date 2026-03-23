# Changelog — V0RTEX

All notable changes are documented here.
Format: `[version] — date — summary`

> `V = Vulnerability · O = Oriented · R = Recon · T = Threat · E = Exploitation · X = eXaminer`

---

## [1.0.1.X0] — 2026-03-23

### Changed
- **Trampoline logic moved from `v0rtex.py` to `v0rtex_adapter.py`** — the `--trampoline-update` block (369 lines) embedded at the top of `v0rtex.py` has been removed entirely. The adapter now owns the full update chain.
- **`v0rtex_adapter.py` is now self-updating** — before starting the splash UI, the adapter fetches its own latest version from `Adapters/v0rtex_adapter.py` on the remote branch. If a newer version is found, it overwrites itself and relaunches with the same arguments, then exits. The new instance continues the update.
- **Trampoline loop integrated into adapter** — after the kill step, the adapter fetches `compat_map.json` from GitHub and runs a hop loop: finds the current version in the chain, installs each intermediate `v0rtex.py` silently (no splash, log only), installs deps, writes `vx_version`, advances to the next hop until the target version is one step away. The final install is handled by the normal 6-step pipeline.
- **Version bump to 1.0.1.X0.**
- **V0RTEX acronym updated** — `V = Vulnerability · O = Oriented · R = Recon · T = Threat · E = Exploitation · X = eXaminer`.

### Removed
- `--trampoline-update` flag and `_trampoline_update_main()` from `v0rtex.py`.

---

## [1.0.0.X0] — 2026-03-23

### Added

#### v0rtex_adapter.py — Post-Update Adapter
- New standalone adapter script spawned by the updater after downloading a new version. Runs entirely outside the main app.
- Reads all parameters from a JSON meta file passed as `sys.argv[1]`: `install_dir`, `python_exe`, `old_version`, `new_version`, `branch`, `manifest`, `vx_system_dir`, `preserve_config`, `emergency_backup_path`, `userdata_backup_path`.
- 6-step pipeline with a live splash UI (step tracker, progress bar, scrolling log terminal, per-package pill feed):
  1. **Kill** — terminates all running V0RTEX processes (psutil + fallback WMIC/taskkill/pgrep)
  2. **Deps** — reads `.vx_meta/.deps_to_remove`, uninstalls obsolete packages
  3. **Pip** — `pip install -r requirements.txt --upgrade` with live per-package progress
  4. **Dirs** — rebuilds the full directory tree
  5. **Meta** — writes `vx_version` JSON
  6. **Launch** — starts `v0rtex.py --v0rtex-post-update --just-updated <old_ver>`. On failure → emergency restore from ZIP → relaunch. Self-deletes via delayed `cmd /c del` on Windows.
- `FRESH_INSTALL` mode: downloads `v0rtex.py` + `requirements.txt` before the pipeline. Supports `DATA_RESET=True` (full wipe) or keep-data mode (preserves `config.json`, `scan_history.db`, `whitelist.txt`, `rules/`, etc.)

#### Trampoline Update System (embedded in `v0rtex.py`, removed in 1.0.1.X0)
- `--trampoline-update <settings_path>` flag activates trampoline mode instead of opening the UI.
- Fetches `compat_map.json` from `{BRANCH}/compat_map.json` on GitHub — defines an ordered chain of intermediate versions with raw download URLs.
- **Each hop (4 steps, silent):**
  1. Installs self into `install_dir`, writes `vx_version`, rebuilds essential dirs
  2. Installs dependencies silently
  3. Fetches `compat_map.json`, reads the chain
  4. Downloads the next version, validates with `ast.parse()`, deletes `v0rtex_system/`, spawns the new version with `--trampoline-update`, self-deletes and exits
- Each hop is a fresh `v0rtex.py` instance running in trampoline mode.
- **Final hop:** installs self, installs deps, restores user data from backup ZIP, writes `vx_version`, shows minimal splash ("FINALIZING UPDATE...", 360×90px topmost). On Windows uses `schtasks` to kill the trampoline and relaunch `v0rtex.py`. On Linux/Mac uses a detached subprocess.

#### NET — New Sub-tabs
- **🔀 PROXY** — HTTP / HTTPS / SOCKS5 proxy manager. ARM / STOP / Test. Persisted to `config.json`.
- **🧅 TOR** — Tor anonymous routing. Auto-detects binary, winget install fallback. Start / Stop / New Identity / Check IP.
- **📡 NOISE GEN** — Network noise generator with live stats.
- **📡 LIVE TRAFFIC** — Real-time per-interface traffic monitor with rolling graph.
- **📊 CONN STATS** — Live connection state graph (ESTABLISHED / TIME_WAIT / CLOSE_WAIT / other).
- **📶 PING** — ICMP ping utility.

#### IOC — New Sub-tab
- **📦 IMPHASH** — PE Import Hash Analyzer for malware family clustering. Single file and bulk folder scan.

#### LOOK — New Sub-tabs
- **🧬 FUZZY** — Fuzzy hash similarity via rolling hash + Jaccard scoring.
- **🔎 BINPAT** — Binary pattern search.

#### CFG — New Sub-tab
- **📜 UPDATE LOG** — Update history from `debug_log/update_log/`.

#### SET — New Sub-tab
- **PRIVACY** — Auto-censor logs toggle, censor category config, `Temp_Log_Storage` management.

#### HOME — New Sub-tab
- **README** — Embedded README viewer.

#### Log Censor System
- `_censor_log_msg()` — redacts sensitive strings from log output when `auto_censor_logs` is enabled.
- `_build_censor_script()` — standalone V0RTEX LOG CENSOR window with rule selection and `censor_config.json` persistence.
- Categories: `api_keys`, `file_paths`, `ip_addresses`, `hashes`, `credentials`, `conn_quality`, `tor`, `proxy`, `noise_gen`.

#### Crash & Exception Handling
- `_early_crash_hook()` — `sys.excepthook` installed before any UI. Writes crash before main handler is ready.
- `_vx_debug_excepthook()` — full crash handler with report and recovery terminal.
- `_tk_callback_exception_handler()` — catches exceptions inside Tkinter callbacks (previously silent).

#### Session Logging
- `_sl_init()` / `_sl_copy_to_final()` — two-phase session log.
- `_app_log_open()` / `_app_log_write()` — named sub-log helpers.

#### Other
- `_SubprocessSilencer` — context manager suppressing subprocess noise.
- `_ap_bk_emergency_rollback()` — emergency rollback button in PROT → BACKUP.
- Lazy tab init for PROC, DBL, SCAN HISTORY — deferred to first focus.
- PROT → System Check: new **🧬 FULL SCAN** sub-tab.

### Changed
- Version bumped from `0.9.9.X0` to `1.0.0.X0`.
- NET: 11 sub-tabs (was 8). LOOK: 18 (was 16). IOC: 9 (was 8).
- Updater now spawns `v0rtex_adapter.py` for post-download phase.

### Fixed
- Tkinter callback exceptions now routed to crash handler.
- Cold-start performance improved via deferred tab init.

---

## [0.9.9.X0] — 2026-03-17

### Added
- **Centralized versioning system** — `_vx_load_ver()` reads `.vx_meta/vx_version` at startup. All 48 hardcoded version strings replaced with variables.
- **Settings → ⚡ PERFORMANCE tab** — throttle scans, max workers, chunk size, thread delay, niceness, cross-link to Advanced.
- **Recovery UI → 🏷 VERSION tab** — reads `vx_version` independently, backup history, rollback picker, Open Updater button.
- **Recovery UI — animated rectangle** — runs during REPAIR, INSTALL PACKAGES, INTEGRITY CHECK. Shows `✓` for 2.5s then returns to idle pulse.
- **Recovery UI — persistent LOG** — saves to `debug_log/recovery_ops/recovery_YYYYMMDD_HHMM.log`.
- **Recovery UI — PRIMARY ACTIONS section** — clean single-row button layout.
- **Standalone `v0rtex_updater.py` rewritten** — Check GitHub, Download & Update, Rebuild Filesystem, Launch V0RTEX.
- **Standalone `v0rtex_recovery_ui.py` rewritten** — REPAIR tab, LAUNCH tab, fully self-contained.
- **Background performance helpers** — `_bg_nice()` and `_bg_scan_delay()` applied to backup, compile, scan and watchdog threads.
- **Crash code 106 `VERSION_MISSING`** — added to `SOC_ERROR_CODES` and Danger Zone.
- **`debug_log/recovery_ops/`** — new subdirectory.

### Changed
- "INSTALLATION MEDIA" → "V0RTEX UTILS" in Recovery UI.
- "Keep admin privileges on startup" removed from Settings.
- Admin required popup now navigates to Settings → Advanced → Startup Privileges.
- System Fixer admin popup — UAC button removed.
- Splash screen `prog_f` `padx` 20 → 12 to fix overflow on small displays.

### Fixed
- Full Scan (DSC) buttons not visible.
- System Fixer buttons not visible — `bot_f` moved before `PanedWindow`. `minsize(700, 500)`.
- Recovery UI REPAIR layout.
- Recovery UI animation stop sequence.
- Standalone updater `_detect_local()` — no longer misidentifies `_ADM_BADGE_*` lines.

### Removed
- Internal melt/self-destruct subsystem removed entirely.

---

## [0.9.8.X2] — 2026-03-15

### Added
- **System Verifier** — PROT → System Check → SCAN: 6-step Windows health check (Defender status, quick malware scan, SFC, DISM, SMART, startup persistence). Split-pane UI, spinner, stall warning, auto-prompt System Fixer.
- **System Fixer** — Full Repair / SFC Only / DISM Only with `indeterminate` progress bar.
- **YARA multi-engine install chain** — `yara-python-wheel` → `yara-x` → VS Build Tools + source.
- **YARA compatibility shim** — `_load_yara()` wraps `yara_x` to expose the `yara-python` API.
- **tshark auto-resolve** — `_resolve_tshark()` checks config → `shutil.which` → registry → known paths.
- **Update UI — step 7/7** — mandatory dep reinstall on every update.

### Changed
- YARA removed from `requirements.txt`.
- Watchdog moved into PROT → System Check.
- Report Builder removed from CFG.
- Update pipeline renumbered to 7 steps.
- All source comments removed.
- All user-facing strings translated to English.

### Fixed
- System Fixer progress bar — `indeterminate` mode.
- Empty SFC output — UTF-16 LE decoding.
- SFC stall — direct call instead of PowerShell pipe.
- YARA MessageBox — `ctypes.windll.user32.MessageBoxW` instead of `tkinter.Tk()` from background thread.
- YARA pip error invisible — WARNING/NOTICE filtered.
- YARA missing from final check — explicit probe added.
- tshark path not saved to config.

### Security
- AV false-positive reduction — sensitive strings assembled at runtime from fragments.

---

## [0.9.7.X3] — 2025

### Added
- Updater version comparator fix — handles alphanumeric tags.
- Dual-file update — patches external launcher if detected.
- Reinstall — local copy default.
- Recovery — Clean TEMP button.
- Crash UI fix — corrected ASCII art.

---

## [0.9.7.X2] and earlier

No changelog kept for versions prior to v0.9.7.X3.
