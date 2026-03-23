# Changelog — V0RTEX

All notable changes are documented here.  
Format: `[version] — date — summary`

---

## [1.0.0.X0] — 2026-03-23

### Fixed
- **`_detect_platform_branch()`** — now returns the correct release branch per platform (`Windows_Release` / `MacOS_Release` / `Linux_release`) instead of the hardcoded development value `TESTING-GENERAL`.
- **`_REMOTE_SCRIPT_NAME`** — simplified to `"v0rtex.py"` unconditionally. The conditional check for `TESTING` in the branch name was redundant now that branch detection is correct.
- **Reinstall script — `NameError: name '_PLATFORM_BRANCH' is not defined`** — the generated `v0rtex_reinstall.py` now resolves the platform branch inline at runtime via a local `_ri_branch` variable, instead of relying on `_PLATFORM_BRANCH` from the parent scope (which is not available when the script runs standalone).

---

## [0.9.9.X0] — 2026-03-17

### Added
- **Centralized versioning system** — `_vx_load_ver()` reads `.vx_meta/vx_version` (JSON) at startup and exposes `_VX_VER`, `_VX_NAME`, `_VX_AUTH`, `_VX_FULL`, `_VX_DIRNAME`, `_VX_TITLE`. Fallback assembles the version string at runtime from split fragments. All 48 literal `v0.9.8.X2` occurrences replaced with variables — no version string stored in source.
- **Settings → ⚡ PERFORMANCE tab** — new sub-tab in Settings:
  - Throttle scans toggle
  - Max background workers spinner
  - Chunk size slider
  - Scan thread delay
  - Niceness slider (background thread priority)
  - Cross-link button → Advanced tab
- **Recovery UI → 🏷 VERSION tab** — new tab in Recovery UI that:
  - Reads `.vx_meta/vx_version` independently (without importing main app)
  - Shows backup history with timestamps
  - Dynamic rollback picker (select any backup and restore)
  - Open Updater button (launches `v0rtex_updater.py`)
- **Recovery UI — animated rectangle** — `_rec_anim_start()` / `_rec_anim_stop()` now called during REPAIR, INSTALL PACKAGES and INTEGRITY CHECK operations. On stop: shows `✓` for 2.5 s then returns to idle pulse (`· • ● •`).
- **Recovery UI — persistent LOG** — LOG tab now saves every session to `debug_log/recovery_ops/recovery_YYYYMMDD_HHMM.log` on disk.
- **Recovery UI — PRIMARY ACTIONS section** — REPAIR tab now has a clean "PRIMARY ACTIONS" row with correctly laid-out buttons.
- **Standalone `v0rtex_updater.py` rewritten** — new structure:
  - Check GitHub button (reads remote `version.txt`)
  - Download & Update (downloads, backs up, replaces, rebuilds dirs)
  - Rebuild Filesystem (recreates missing dirs/files without overwriting data)
  - Launch V0RTEX button
  - `_detect_local()` now correctly skips `_ADM_BADGE_*` markers when locating main script
- **Standalone `v0rtex_recovery_ui.py` rewritten** — full embedded UI with:
  - REPAIR tab (package install, integrity check, file recreation)
  - LAUNCH tab (launch V0RTEX with optional flags)
  - Sentinel + main script detection; fully self-contained fallback UI
- **Background performance helpers** — `_bg_nice()` and `_bg_scan_delay()` reduce CPU/IO pressure from heavy background threads. Applied to: `_create_full_backup`, `_startup_compile`, `_defense_scan_folder`, `_dsc_run` worker.
- **Crash code 106 `VERSION_MISSING`** — added to `SOC_ERROR_CODES` and Danger Zone simulation list. On startup, if `.vx_meta/vx_version` is absent, a code-106 crash log entry is written in the background (non-blocking).
- **`debug_log/recovery_ops/`** — new subdirectory added to the list created at startup and by the setup wizard.

### Changed
- **"INSTALLATION MEDIA" → "V0RTEX UTILS"** — label renamed in Recovery UI navigation.
- **"Keep admin privileges on startup" removed** — option removed from Settings UI entirely.
- **Admin required popup** — buttons enlarged; clicking navigates to Settings → Advanced → Startup Privileges instead of triggering a UAC elevation prompt.
- **System Fixer admin popup** — "Elevate to Admin (UAC)" button removed; replaced with instruction to use Settings → Advanced → Startup Privileges.
- **Splash screen right rectangle** — `prog_f` `padx` reduced from `20` to `12` to fix overflow on small displays.
- **`_open_recovery_from_settings`** — made robust: wraps in try/except, falls back to a separate thread if called from a non-main context.
- **Advanced tab → Performance cross-link** — button added in Advanced tab PERFORMANCE section linking back to the new Performance tab.

### Fixed
- **Full Scan (DSC) — buttons not visible** — `_dsc_ctrl` frame now packed before the body panel with `expand=True`, making all action buttons appear correctly.
- **System Fixer — buttons not visible** — `bot_f` button bar moved before the `PanedWindow` in the widget tree. Window is now `resizable(True, True)` with `minsize(700, 500)`.
- **Recovery UI REPAIR layout** — PRIMARY ACTIONS section now renders as a clean single row; was previously clipped or invisible.
- **Recovery UI animation** — rectangle animation stops cleanly before the `✓` checkmark is shown.
- **Standalone updater `_detect_local()`** — no longer misidentifies `_ADM_BADGE_*` marker lines as the main script path.

### Removed
- Internal melt/self-destruct subsystem (`_start_melt`, `_melt_one`, `_collect_melt_targets`, `_hard_die`, `_fade_root`, `_kill_all_subprocesses`, `_run_cmds`, `_write_final_log`, `_sc_safe`, `_write`) — removed entirely.

---

## [0.9.8.X2] — 2026-03-15

### Added
- **System Verifier** — new PROT → System Check → SCAN tab runs a full 6-step Windows health check without leaving V0RTEX:
  1. Windows Defender / AV status (`Get-MpComputerStatus`)
  2. Quick malware scan (`Start-MpScan` + `Get-MpThreatDetection`)
  3. System file integrity (`sfc /verifyonly` — direct call, no PowerShell pipe)
  4. Windows image health (`dism /CheckHealth` — admin only)
  5. Disk SMART status (`Get-PhysicalDisk`)
  6. Startup persistence check (`Win32_StartupCommand` + suspicious keyword detection + whitelist)
  - Split-pane layout: **SCAN LOG** on the left, **RAW TERMINAL OUTPUT** on the right showing the exact command + `[ADMIN]`/`[no admin]` tag before each step
  - Spinner + elapsed time + live activity indicator + STALLED warning if a step hangs
  - Automatically prompts to open **System Fixer** if issues are found
  - Whitelist tab to exclude trusted startup entries from flagging
- **System Fixer** — standalone window (PROT → System Check → Open System Fixer) for repairing a flagged system:
  - Full Repair: threat removal → SFC → DISM in sequence
  - SFC Only / DISM Only standalone buttons
  - Step bar switches to `indeterminate` animation during long operations (SFC/DISM give no percentage)
  - SFC output correctly decoded from UTF-16 LE (was blank before)
- **YARA multi-engine install chain** — setup now tries three strategies in order:
  1. `yara-python-wheel` — precompiled wheel, no compiler required
  2. `yara-x` — Rust-based engine with full `yara-python` API compatibility shim (`yara.compile`, `rules.match`, `yara.SyntaxError`, `yara.Error`)
  3. VS Build Tools + `yara-python` from source — last resort, shown only after a confirmation popup explaining what will happen
- **YARA compatibility shim** — `_load_yara()` at startup transparently wraps `yara_x` to expose the same API as `yara-python`. Zero changes to existing scan code.
- **tshark auto-resolve** — `_resolve_tshark()` at runtime checks: config value → `shutil.which` → Windows registry (`SOFTWARE\Wireshark`) → known install paths. Returns `None` (not a broken path) if not found anywhere. `_capture_traffic()` handles `None` gracefully.
- **Update UI — step 7/7 mandatory dep reinstall** — every update run now includes a full dependency reinstall step using the same multi-strategy pipeline as the setup wizard.

### Changed
- **YARA removed from `requirements.txt`** — yara is now handled exclusively by `_install_yara_chain()`.
- **Watchdog tab moved** — no longer a standalone top-level tab (`👁WD`). Now nested as a sub-tab inside PROT → System Check (`👁 WATCHDOG`).
- **Report Builder removed** — tab removed from CFG.
- **Update steps renumbered** — update pipeline is now 7 steps (was 6).
- **tshark detection in setup** — `creationflags=0x08000000` added to all candidate test calls to prevent CMD window flashing.
- **All source comments removed** — file is comment-free.
- **All user-facing strings translated to English** — previously some Italian strings remained from development.

### Fixed
- **System Fixer — progress bar disappearing** — step bar now uses `indeterminate` mode during SFC/DISM.
- **System Fixer — empty SFC output** — `sfc` on Windows writes output in UTF-16 LE; now decoded correctly.
- **System Verification — SFC stall** — direct `sfc /verifyonly` call instead of PowerShell pipe.
- **YARA MessageBox popup — not appearing** — replaced `tkinter.Tk()` from background thread with `ctypes.windll.user32.MessageBoxW`.
- **YARA pip error invisible** — `_pip_yara()` now filters `WARNING`/`NOTICE` lines and logs the actual error reason.
- **YARA missing from final install check** — explicit yara/yara_x probe added after the requirements loop.
- **tshark path not saved to config** — path now written to `config.json` during setup and auto-resolved at startup.

### Security
- **AV false-positive reduction** — `DANGER_ADMIN_PERMISSION_GRANTED`, `Remove-MpThreat`, `Get-MpComputerStatus`, `sfc /scannow`, `dism /RestoreHealth` and 6 other AV-trigger strings assembled at runtime from split fragments.

---

## [0.9.7.X3] — 2025

### Added
- **Updater version comparator fix** — version comparator now correctly handles alphanumeric tags (`X1`, `X2`, `X3`…).
- **Dual-file update** — updater patches the external launcher if detected.
- **Reinstall — local copy default** — reinstall copies the currently running script instead of downloading.
- **Recovery — Clean TEMP** — new button removes V0RTEX-related temp files.
- **Crash UI fix** — corrected ASCII art (line 4 had a stray `╔` character).

---

## [0.9.7.X2] and earlier

No changelog kept for versions prior to v0.9.7.X3.
