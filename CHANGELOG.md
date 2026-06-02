# Changelog — V0RTEX

All notable changes are documented here.
Format: `[version] — date — summary`

> `V = Vulnerability · O = Oriented · R = Recon · T = Threat · E = Exploitation · X = eXaminer`

---

## [1.1.1.X0] — 2026-06-03

### Added

#### AI Core Module
- **Intelligent Threat Analysis Engine** — Integrated a local AI subsystem designed for semantic context mapping, heuristic anomaly detection, and correlation of extracted indicators.
- **Context-Aware Vulnerability Mapping** — Dynamic mapping of scan targets against contextual exploit chains based on intelligence parsed by the new core.

#### Sandbox Protection & Anti-Analysis
- **Guardian Environment Monitor** — Proactive, multi-layered background agent tasked with continuous verification of the execution environment (detecting automated sandboxes, debugging hooks, and analysis artifacts).
- **Automated Panic System** — Emergency panic routine programmed to gracefully intercept runtime bypass attempts, state corruption, or memory manipulation, freezing execution states before exposure.
- **Forensic Self-Destruct Sequence** — High-integrity, secure deletion routine engineered to instantly purge volatile data storage, encryption keys, and operational logs inside `Temp_Log_Storage` in hostile execution environments.

#### Scanning & Core Vectors
- **Universal Processing Functions** — Refactored low-level analysis loops into highly generic, modular functions to maximize reuse across different modules.
- **Advanced Deobfuscation & Scanning Algorithms** — Added novel decoding routines and signature-matching helpers to effectively analyze heavily packed, obfuscated, or legacy malware data streams.

### Changed
- Version bumped to 1.1.1.X0.

---

## [1.0.1.X1] — 2026-03-23

### Fixed
- **`debug_log` no longer created inside the install directory** — five separate code paths were incorrectly creating `debug_log/` and its subdirectories inside `V0RTEX_vX.X.X.XX/` instead of `v0rtex_utils/debug_log/`. All fixed:
  - `_setup_panic` (pre-init crash hook) — now resolves `DEBUG_DIR` from globals with fallback to `v0rtex_utils/debug_log/crash_log`
  - `_REQUIRED_DIRS` at startup — `debug_log` fallback to `BASE_DIR` removed; `DEBUG_DIR` already points to `v0rtex_utils`
  - In-app updater `_std_dirs` — `debug_log` removed from install dir list; subdirs now created in `v0rtex_utils/debug_log`
  - Recovery Selective Regeneration — same fix as updater
  - `_run_silent_update_ui` (post-update setup) — `debug_log` removed from `install_dir` loop; created in `v0rtex_utils/debug_log`

### Changed
- Version bumped to 1.0.1.X1.

---

## [1.0.1.X0] — 2026-03-23

### Changed
- **Trampoline logic moved from `v0rtex.py` to `v0rtex_adapter.py`** — the `--trampoline-update` block (369 lines) embedded at the top of `v0rtex.py` has been removed entirely. The adapter now owns the full update chain.
- **`v0rtex_adapter.py` is now self-updating** — before starting the splash UI, the adapter fetches its own latest version from `Adapters/v0rtex_adapter.py` on the remote branch. If a newer version is found, it overwrites itself and relaunches with the same arguments, then exits.
- **Trampoline loop integrated into adapter** — after the kill step, the adapter fetches `compat_map.json` from GitHub and runs a hop loop: finds the current version in the chain, installs each intermediate `v0rtex.py` silently (no splash, log only), installs deps, writes `vx_version`, advances to the next hop until the target version is one step away. The final install is handled by the normal 6-step pipeline.
- **Version bump to 1.0.1.X0.**
- **V0RTEX acronym updated** — `V = Vulnerability · O = Oriented · R = Recon · T = Threat · E = Exploitation · X = eXaminer`.

### Removed
- `--trampoline-update` flag and `_trampoline_update_main()` from `v0rtex.py`.

---

## [1.0.0.X0] — 2026-03-23

### Added

#### v0rtex_adapter.py — Post-Update Adapter
- New standalone adapter script spawned by the updater after downloading a new version.
- Reads all parameters from a JSON meta file passed as `sys.argv[1]`: `install_dir`, `python_exe`, `old_version`, `new_version`, `branch`, `manifest`, `vx_system_dir`, `preserve_config`, `emergency_backup_path`, `userdata_backup_path`.
- 6-step pipeline with a live splash UI (step tracker, progress bar, scrolling log terminal, per-package pill feed):
  1. **Kill** — terminates all running V0RTEX processes (psutil + fallback WMIC/taskkill/pgrep)
  2. **Deps** — reads `.vx_meta/.deps_to_remove`, uninstalls obsolete packages
  3. **Pip** — `pip install -r requirements.txt --upgrade` with live per-package progress
  4. **Dirs** — rebuilds the full directory tree
  5. **Meta** — writes `vx_version` JSON
  6. **Launch** — starts `v0rtex.py --v0rtex-post-update --just-updated <old_ver>`. On failure → emergency restore from ZIP → relaunch. Self-deletes via delayed `cmd /c del` on Windows.
- `FRESH_INSTALL` mode: downloads `v0rtex.py` + `requirements.txt` before the pipeline. Supports `DATA_RESET=True` (full wipe) or keep-data mode (preserves `config.json`, `scan_history.db`, `whitelist.txt`, `rules/`, etc.)

#### Trampoline Update System (embedded in `v0rtex.py`, moved to adapter in 1.0.1.X0)
- `--trampoline-update <settings_path>` flag activates trampoline mode instead of opening the UI.
- Fetches `compat_map.json` from `{BRANCH}/compat_map.json` — defines an ordered chain of intermediate versions with raw download URLs.
- Each hop: installs self, installs deps silently, downloads next version, validates with `ast.parse()`, deletes `v0rtex_system/`, spawns new version with `--trampoline-update`, self-deletes.
- Final hop: installs self, restores user data from backup ZIP, writes `vx_version`, shows minimal splash, uses `schtasks` on Windows to kill trampoline and relaunch `v0rtex.py`.

#### NET — New Sub-tabs
- **🔀 PROXY** — HTTP/HTTPS/SOCKS5 proxy manager. ARM / STOP / Test.
- **🧅 TOR** — Tor anonymous routing. Auto-detect, winget install fallback. Start / Stop / New Identity / Check IP.
- **📡 NOISE GEN** — Network noise generator with live stats.
- **📡 LIVE TRAFFIC** — Real-time per-interface traffic monitor with rolling graph.
- **📊 CONN STATS** — Live connection state graph (ESTABLISHED / TIME_WAIT / CLOSE_WAIT / other).
- **📶 PING** — ICMP ping utility.

#### IOC — New Sub-tab
- **📦 IMPHASH** — PE Import Hash Analyzer for malware family clustering.

#### LOOK — New Sub-tabs
- **🧬 FUZZY** — Fuzzy hash similarity via rolling hash + Jaccard scoring.
- **🔎 BINPAT** — Binary pattern search.

#### CFG — New Sub-tab
- **📜 UPDATE LOG** — Update history from `debug_log/update_log/`.

#### SET — New Sub-tab
- **PRIVACY** — Auto-censor logs, per-category rules, `Temp_Log_Storage` management.

#### HOME — New Sub-tab
- **README** — Embedded README viewer.

#### Log Censor System
- `_censor_log_msg()`, `_build_censor_script()`, `_open_log_censor()`, `_priv_autocensor_toggle()`.
- Categories: `api_keys`, `file_paths`, `ip_addresses`, `hashes`, `credentials`, `conn_quality`, `tor`, `proxy`, `noise_gen`.

#### Crash & Exception Handling
- `_early_crash_hook()`, `_vx_debug_excepthook()`, `_tk_callback_exception_handler()`.

#### Session Logging
- `_sl_init()` / `_sl_copy_to_final()` — two-phase session log.
- `_app_log_open()` / `_app_log_write()`.

#### Other
- `_SubprocessSilencer` — context manager suppressing subprocess noise.
- `_ap_bk_emergency_rollback()` — emergency rollback in PROT → BACKUP.
- Lazy tab init for PROC, DBL, SCAN HISTORY.
- PROT → System Check: new **🧬 FULL SCAN** sub-tab.

### Changed
- Version bumped from `0.9.9.X0` to `1.0.0.X0`.
- NET: 11 sub-tabs (was 8). LOOK: 18 (was 16). IOC: 9 (was 8).
- Updater now spawns `v0rtex_adapter.py` for the post-download phase.

### Fixed
- Tkinter callback exceptions now routed to crash handler.
- Cold-start performance improved via deferred tab init.

---

## [0.9.9.X0] — 2026-03-17

### Added
- **Centralized versioning system** — `_vx_load_ver()` reads `.vx_meta/vx_version` at startup. All 48 hardcoded version strings replaced with variables.
- **Settings → ⚡ PERFORMANCE tab** — throttle scans, max workers, chunk size, thread delay, niceness, cross-link to Advanced.
- **Recovery UI → 🏷 VERSION tab** — reads `vx_version` independently, backup history, rollback picker, Open Updater button.
- **Recovery UI** — animated rectangle, persistent LOG, PRIMARY ACTIONS section.
- **Standalone `v0rtex_updater.py` rewritten** — Check GitHub, Download & Update, Rebuild Filesystem, Launch V0RTEX.
- **Standalone `v0rtex_recovery_ui.py` rewritten** — REPAIR tab, LAUNCH tab, fully self-contained.
- **Background performance helpers** — `_bg_nice()` and `_bg_scan_delay()`.
- **Crash code 106 `VERSION_MISSING`**.
- **`debug_log/recovery_ops/`** — new subdirectory.

### Changed
- "INSTALLATION MEDIA" → "V0RTEX UTILS".
- "Keep admin privileges on startup" removed.
- Admin popup navigates to Settings → Advanced → Startup Privileges.
- Splash screen `padx` 20 → 12.

### Fixed
- Full Scan (DSC) buttons not visible.
- System Fixer buttons not visible. `minsize(700, 500)`.
- Recovery UI REPAIR layout and animation.
- Standalone updater `_detect_local()`.

### Removed
- Internal melt/self-destruct subsystem removed entirely.

---

## [0.9.8.X2] — 2026-03-15

### Added
- **System Verifier** — PROT → System Check → SCAN: 6-step Windows health check (Defender, quick scan, SFC, DISM, SMART, startup persistence). Split-pane UI, spinner, stall warning, auto-prompt System Fixer.
- **System Fixer** — Full Repair / SFC Only / DISM Only.
- **YARA multi-engine install chain** — `yara-python-wheel` → `yara-x` → VS Build Tools + source.
- **YARA compatibility shim** — `_load_yara()` wraps `yara_x` to expose the `yara-python` API.
- **tshark auto-resolve** — `_resolve_tshark()`.
- **Update UI — step 7/7** — mandatory dep reinstall on every update.

### Changed
- YARA removed from `requirements.txt`.
- Watchdog moved into PROT → System Check.
- Report Builder removed from CFG.
- Update pipeline renumbered to 7 steps.
- All source comments removed. All strings translated to English.

### Fixed
- System Fixer progress bar, SFC UTF-16 LE decoding, SFC stall, YARA MessageBox, YARA pip error, tshark path not saved.

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
