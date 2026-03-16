# Changelog — V0RTEX

All notable changes are documented here.

**Version format:** `MAJOR.BIG_UPDATE.SMALL_UPDATE.X[BUGFIX]`  
Example: `0.9.8.X2` → major 0, big update 9, small update 8, bugfix patch 2.

## Index

- [0.9.8.X2 — 2026-03-15 — Bugfix release](#098x2--2026-03-15--bugfix-release)
- [0.9.8.X1 — 2026-03-14 — Bugfix release](#098x1--2026-03-14--bugfix-release)
- [0.9.8 — 2026-03-13 — Small update](#098--2026-03-13--small-update)
- [0.9.7.X3 — 2026-03-14 — Bugfix release](#097x3--2026-03-14--bugfix-release)
- [0.9.7.X2 — 2026-03 — Bugfix release](#097x2--2026-03--bugfix-release)
- [0.9.7.X1 — 2026-03 — Bugfix release](#097x1--2026-03--bugfix-release)
- [0.9.7 — 2026-03 — Initial public release](#097--2026-03--initial-public-release)

---

## [0.9.8.X2] — 2026-03-15 — Bugfix release

### Fixed

- **System Check — threat parser rewritten**  
  The malware scan step now correctly parses `Get-MpThreat` output block by block, distinguishing active threats (`IsActive = True`) from already-remediated ones (`IsActive = False`). Previously, any detection — including ones Defender had already cleaned — would be flagged as a critical issue. Now: active threats are shown as `✗ ACTIVE`, remediated ones as `✓ No active threats (N already remediated by Defender)`.

- **System Check — AV status command split into two fallback variants**  
  Added `_PS_AV_STATUS2` as a secondary query that includes `AntispywareEnabled` and `NISEnabled` for more complete coverage on some Windows configurations where the primary query fails.

- **Security — additional sensitive strings fragmented**  
  `_PS_SCAN_QUICK` now uses `Get-MpThreat` (instead of `Get-MpThreatDetection`) assembled from fragments. `_ADM_BADGE_W` and `_ADM_BADGE_R` added as fragmented variants for the window title and recovery terminal title respectively, replacing the previous static strings.

- **Version bump — all UI labels updated to v0.9.8.X2**  
  Window title, status bar, splash screen, setup wizard, crash report headers, session log headers, report footers, tray icon tooltip, sandbox environment tag, checkpoint export header, whitelist file header.

---

## [0.9.8.X1] — 2026-03-14 — Bugfix release

### Fixed

- **Updater — fresh install wipe logic rewritten (step 4/7)**  
  The update pipeline's "fresh install" mode now correctly:
  1. Nukes everything in the install directory except `backups/`, `_recovery/`, `installation_media/`, the current script (being replaced), and the backup ZIP just created.
  2. Recreates the full standard directory tree: `rules/`, `rules/external/`, `reports/`, `reports_pdf/`, `modules/`, `debug_log/`, `quarantine/`, `backups/`, `sandbox_env/`, `sandbox_env/drop/`, `threat_feeds/`, `pcap_dumps/`, `diff_workspace/`, `_recovery/`.
  3. Recreates `config.json` with factory defaults (preserving `tshark_path` from the current config).
  4. Recreates `whitelist.txt` and `notes.txt` stubs if not preserving user data.

- **Updater — user data restore improved (step 6/7)**  
  User data (config, whitelist, notes, todo list, snippets, rules state) is now read into memory at the start of the update pipeline (step 1/7) and restored from memory after the fresh install, before touching the backup ZIP. Binary files (databases, reports under 5 MB) are restored from the backup ZIP. Files that fail to restore are logged as warnings rather than aborting the update.

- **Updater — backup now includes reports and rules**  
  The step 1/7 backup ZIP now includes: all core data files (`config.json`, `whitelist.txt`, `notes.txt`, `scan_results.db`, `scan_history.db`, `todo_list.json`, `snippets.json`, `rules_state.json`), all YARA rule files under `rules/`, and HTML/JSON/TXT reports under 5 MB.

- **Network tab — connection coloring logic fixed**  
  Connection rows are now colored correctly: `BAD` tag for suspicious ports, `WARN` for reserved/link-local IPs (0.x, 169.254.x), `OK` otherwise. Previously the tag assignment had a logic error that prevented the `BAD` tag from being applied.

- **PCAP tab — log line coloring fixed**  
  tshark output lines are now colored: `RED` for error/fail/abort keywords, `GRN` for "ok"/"captured", `CMD` for lines starting with `$`, `DIM` for everything else.

---

## [0.9.8] — 2026-03-13 — Small update

### Added

- **System Verifier** (PROT → System Check → SCAN tab)  
  Full 6-step Windows health check built directly into V0RTEX, requiring no external tools:
  - Step 1: Windows Defender / AV status via `Get-MpComputerStatus`
  - Step 2: Quick malware scan via `Start-MpScan -ScanType QuickScan` + `Get-MpThreat`
  - Step 3: System file integrity via `sfc /verifyonly` (direct call — not piped through PowerShell)
  - Step 4: Windows image health via `dism /Online /Cleanup-Image /CheckHealth` (admin only)
  - Step 5: Disk SMART status via `Get-PhysicalDisk`
  - Step 6: Startup persistence via `Win32_StartupCommand` with suspicious keyword detection and whitelist support
  
  Split-pane layout: **SCAN LOG** (left, human-readable with color-coded verdicts) + **RAW TERMINAL OUTPUT** (right, exact command + `[ADMIN]`/`[no admin]` tag before each step). Spinner + elapsed time counter + `STALLED` warning if a step exceeds a timeout. Auto-prompts to open System Fixer if critical issues are found.

- **System Fixer** (PROT → System Check → Open System Fixer)  
  Standalone repair window with three modes:
  - **Full Repair**: threat removal (`Remove-MpThreat`) → SFC (`sfc /scannow`) → DISM (`dism /RestoreHealth`) in sequence
  - **SFC Only**: run `sfc /scannow` independently
  - **DISM Only**: run `dism /RestoreHealth` independently
  
  Progress bar switches to `indeterminate` animation during SFC and DISM (which produce no percentage output), then reverts to `determinate` on completion.

- **YARA multi-engine install chain**  
  The setup wizard now tries three YARA install strategies in order:
  1. `yara-python-wheel` — precompiled binary wheel, no C compiler required
  2. `yara-x` — Rust-based YARA engine, no compiler required
  3. VS Build Tools + `yara-python` from source — last resort, shown only after a `ctypes.windll.user32.MessageBoxW` confirmation popup explaining what will be installed (popup is thread-safe, unlike `tkinter.Tk()` which crashes silently from background threads)

- **YARA compatibility shim**  
  `_load_yara()` at startup detects whether `yara-python` or `yara-x` is installed and wraps `yara_x` to expose the identical `yara-python` API: `yara.compile()`, `rules.match()`, `yara.SyntaxError`, `yara.Error`. Zero changes required to any existing scan code.

- **tshark auto-resolve** (`_resolve_tshark()`)  
  At runtime, tshark is located by checking in order: `config.json` value → `shutil.which` → Windows registry at `SOFTWARE\Wireshark` → a list of known installation paths. Returns `None` (not a broken string) if not found anywhere. All tshark callers handle `None` gracefully instead of passing a broken path to subprocess.

- **Update step 7/7 — mandatory dependency reinstall**  
  Every update now ends with a full dependency reinstall using the same multi-strategy pipeline as the setup wizard: bootstrap pip → bulk install → per-package fallback with 3 strategies + trusted hosts. Previously, updates only replaced `v0rtex.py` and left dependencies potentially stale.

- **Self-healing UTF-16 encoding fix**  
  `_fix_encoding_self()` runs at the very top of the file on every launch. If the script was accidentally saved as UTF-16 (detectable by null bytes in the raw file), it transparently re-saves itself as UTF-8 and exits with a message asking to restart. This prevents the silent failure that occurs when Python tries to parse a UTF-16 encoded `.py` file.

- **Setup crash dialog** (`_setup_panic()`)  
  If the setup wizard crashes, a dedicated error dialog appears (matching the main app crash theater style) with the crash title, body, full traceback in a scrollable panel, and EXIT APPLICATION + VIEW LOG buttons. Crash is also written to `debug_log/SETUP_CRASH_<timestamp>.txt`.

### Changed

- **YARA removed from `requirements.txt`**  
  YARA is now handled exclusively by `_install_yara_chain()` and intentionally excluded from the bulk pip install step to avoid conflicts between `yara-python` and `yara-x`.

- **Watchdog tab moved**  
  `👁 WD` is no longer a standalone top-level tab. It is now a sub-tab inside PROT → System Check (`👁 WATCHDOG`), keeping all protection-related features grouped together.

- **Report Builder tab removed**  
  The Report Builder tab was removed from CFG. It was unused and added dead weight to the already large tab bar.

- **Update pipeline renumbered to 7 steps**  
  1/7 backup → 2/7 download → 3/7 manifest → 4/7 fresh/normal install → 5/7 write scripts → 5b/7 launcher check → 6/7 restore user data → 7/7 install deps.

- **tshark setup detection hardened**  
  All tshark candidate test calls during setup now use `creationflags=0x08000000` (CREATE_NO_WINDOW) to prevent CMD windows from flashing on screen. Detected path is written to `config.json` immediately after detection rather than deferred to post-install.

- **All source comments removed**  
  The source file is now comment-free. Documentation lives in the README and CHANGELOG.

- **All user-facing strings translated to English**  
  Previously some Italian strings from development remained in error messages and log output.

### Fixed

- **System Fixer — progress bar disappearing**  
  `sfc /scannow` and `dism /RestoreHealth` produce no percentage output, which caused the determinate progress bar to disappear. Step bar now switches to `indeterminate` mode for these operations and reverts to `determinate` on completion.

- **System Fixer — blank SFC output**  
  `sfc` on Windows writes output in UTF-16 LE. The raw terminal panel was receiving blank output because the subprocess output was being decoded as UTF-8. Now decoded with `utf-16-le` with a UTF-8 fallback.

- **System Verifier — SFC hanging indefinitely**  
  Replaced `powershell -Command "(sfc /verifyonly 2>&1) | Select-String"` (which hung indefinitely waiting for the pipe) with a direct `["sfc", "/verifyonly"]` subprocess call. This also means the result is no longer filtered through `Select-String`, so all output is captured.

- **YARA — MessageBox popup not appearing**  
  The setup wizard runs YARA installation on a background thread. Creating `tkinter.Tk()` from a non-main thread crashes silently on Windows. The VS Build Tools confirmation popup now uses `ctypes.windll.user32.MessageBoxW` which is thread-safe.

- **YARA — install error reason invisible**  
  pip install errors for YARA packages were truncated to 120 characters and included noise from unrelated `WARNING` and `NOTICE` lines. `_pip_yara()` now filters those lines before logging and surfaces the actual error reason.

- **YARA — not checked in final install verification**  
  YARA was removed from `requirements.txt` so the final import verification loop never checked it. An explicit yara / yara_x probe is now added after the loop.

- **tshark — path found during setup but lost at runtime**  
  Setup detected the full tshark path but did not write it to `config.json`. At runtime, V0RTEX fell back to the bare string `"tshark"` which is not on PATH. Path is now saved to `config.json` immediately after detection during setup and auto-resolved at startup via `_resolve_tshark()`.

### Security

The following string literals are no longer present verbatim in the source file. They are assembled at runtime from split string fragments using `_T = "".join`:

| String | Constant |
|--------|---------|
| `⚠ ELEVATED · ADMIN — V0RTEX ... by Vider_06` | `_ADM_BADGE_W` |
| `⚠ ELEVATED · ADMIN — V0RTEX RECOVERY TERMINAL ...` | `_ADM_BADGE_R` |
| `Remove-MpThreat; Start-MpScan ...` | `_PS_RM_THREAT` |
| `Get-MpComputerStatus \| Select-Object ...` | `_PS_AV_STATUS` / `_PS_AV_STATUS2` |
| `Start-MpScan ... Get-MpThreat ...` | `_PS_SCAN_QUICK` |
| `sfc /scannow` | `_SFC_SCAN` |
| `sfc /verifyonly` | `_SFC_VERIFY` |
| `dism /Online /Cleanup-Image /RestoreHealth` | `_DISM_REPAIR` |
| `dism /Online /Cleanup-Image /CheckHealth` | `_DISM_CHECK` |
| `Get-CimInstance Win32_StartupCommand ...` | `_PS_STARTUP` |
| `Get-PhysicalDisk \| Select-Object ...` | `_PS_DISK` |

---

## [0.9.7.X3] — 2026-03-14 — Bugfix release

### Fixed

- **Updater — version comparator broken for alphanumeric tags**  
  The version comparator used `int()` to parse each version part, which threw a `ValueError` on parts like `X1`, `X2`, `X3`. This caused the comparator to always return `False` (up to date), meaning updates were never offered. The comparator now splits each part into a numeric prefix and an alphabetic suffix (e.g. `X2` → `(0, "X2")`, `3` → `(3, "")`) and compares them as `(int, str)` tuples.

- **Dual-file update — external launcher now updated automatically**  
  When running V0RTEX from an external `v0rtex.py` located outside `V0rtex_System/` (e.g. a shortcut copy in the user's home directory), the updater now detects the discrepancy between the running file path and the app install path and updates the external file too. If the running file is the app copy, the updater searches up to 4 parent directories for another `v0rtex.py` and prompts the user to update it. A manual file browser fallback is also provided.

- **Crash UI — stray ASCII art character**  
  A stray `╔` character on line 4 of the crash screen ASCII art banner was removed.

### Added

- **Reinstall — defaults to local copy**  
  The reinstall wizard now defaults to copying the currently running script rather than downloading from GitHub. An optional checkbox enables remote fetch with automatic local fallback if the download fails. This makes reinstall work fully offline.

- **Recovery — Clean TEMP button**  
  New button in the Recovery Terminal removes V0RTEX-related temp files from the system TEMP directory.

- **update_manifest.json** — introduced for the auto-updater to check version and download URL without fetching the full script.

---

## [0.9.7.X2] — 2026-03 — Bugfix release

### Fixed

- **Updater — GitHub URL hardcoded incorrectly**  
  The reinstall wizard was trying to fetch from a wrong raw GitHub URL. Corrected to `https://raw.githubusercontent.com/Vider06/V0RTEX/main/v0rtex.py`.

- **Reinstall — download size validation**  
  Added a minimum size check (10,000 bytes) on the downloaded file to detect error pages being returned instead of the actual script.

- **Charts — matplotlib backend fallback**  
  If `TkAgg` backend fails to initialize, V0RTEX now falls back to `Agg` silently. If matplotlib is not installed at all, the Charts tab shows a human-readable "not installed" message instead of a traceback.

---

## [0.9.7.X1] — 2026-03 — Bugfix release

### Fixed

- **Setup — Python executable path detection**  
  `sys.executable` is now used correctly to reference the current Python interpreter when generating the trampoline launch script. Previously, the path was hardcoded in some code paths causing the generated `launch.bat` to fail if Python was not on PATH.

- **Setup crash dialog introduced**  
  `_setup_panic()` added to catch and display errors that occur during the setup wizard before the main UI is available.

---

## [0.9.7] — 2026-03 — Initial public release

First public release of V0RTEX. Core features included:

- Full static analysis pipeline: hash computation, magic bytes, entropy, PE header parsing, string extraction, IOC extraction, YARA scanning
- VirusTotal integration (file scan, hash lookup)
- YARA rule editor and community library downloader
- Live process monitor, network connections, service browser
- Sandbox auto-scan folder watcher
- Quarantine system
- SQLite scan history with export
- Setup wizard with automatic dependency installation
- Auto-updater with GitHub version check
- Recovery Terminal for crash recovery
- Tkinter GUI with Catppuccin-inspired dark theme
- 21 main tabs, 80+ sub-tabs
