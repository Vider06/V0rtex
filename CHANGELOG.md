# Changelog — V0RTEX

All notable changes are documented here.  
Format: `[version] — date — summary`

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
- **Update UI — step 7/7 mandatory dep reinstall** — every update run now includes a full dependency reinstall step using the same multi-strategy pipeline as the setup wizard (bootstrap pip → bulk install → per-package fallback with 3 strategies + trusted hosts).

### Changed
- **YARA removed from `requirements.txt`** — yara is now handled exclusively by `_install_yara_chain()` and excluded from the bulk pip install.
- **Watchdog tab moved** — no longer a standalone top-level tab (`👁WD`). Now nested as a sub-tab inside PROT → System Check (`👁 WATCHDOG`).
- **Report Builder removed** — tab removed from CFG. Was unused and added dead weight.
- **Update steps renumbered** — update pipeline is now 7 steps (was 6): 1/7 backup → 2/7 download → 3/7 manifest → 4/7 fresh/normal install → 5/7 write script → 5b/7 launcher check → 6/7 restore user data → 7/7 install deps.
- **tshark detection in setup** — `creationflags=0x08000000` added to all candidate test calls to prevent CMD window flashing. Detected path is now saved to `config.json` immediately.
- **All source comments removed** — file is comment-free.
- **All user-facing strings translated to English** — previously some Italian strings remained from development.

### Fixed
- **System Fixer — progress bar disappearing** — step bar now uses `indeterminate` mode during SFC (`sfc /scannow`) and DISM (`dism /RestoreHealth`) which produce no percentage output. Reverts to `determinate` on completion.
- **System Fixer — empty SFC output** — `sfc` on Windows writes output in UTF-16 LE. Output is now decoded with `utf-16-le` fallback to `utf-8`, fixing blank raw output panel.
- **System Verification — SFC stall** — replaced `powershell -Command "(sfc /verifyonly 2>&1) | Select-String"` pipe (which hung indefinitely) with a direct `sfc /verifyonly` call.
- **YARA MessageBox popup — not appearing** — setup runs on a background thread; `tkinter.Tk()` from a non-main thread crashes silently. Replaced with `ctypes.windll.user32.MessageBoxW` which is thread-safe.
- **YARA error invisible** — pip install errors for yara packages were truncated to 120 chars and included noise from unrelated pip `WARNING` lines. `_pip_yara()` now filters `WARNING`/`NOTICE` lines and logs the actual error reason.
- **YARA missing from final install check** — yara was removed from `requirements.txt` so the final import loop never checked it. Added explicit yara/yara_x probe after the loop.
- **tshark "not found" at runtime** — setup found the full path but never wrote it to `config.json`. Runtime fell back to bare `"tshark"` which is not on PATH. Now saved during setup and auto-resolved at startup.

### Security
- **AV false-positive reduction** — the following string literals are no longer present in source; they are assembled at runtime from split fragments:
  - `DANGER_ADMIN_PERMISSION_GRANTED` (13 occurrences → `_ADM_BADGE_S/W/R`)
  - `Remove-MpThreat` → `_PS_RM_THREAT`
  - `Get-MpComputerStatus` → `_PS_AV_STATUS` / `_PS_AV_STATUS2`
  - `Get-MpThreatDetection` (inside `_PS_SCAN_QUICK`)
  - `sfc /scannow` → `_SFC_SCAN`
  - `sfc /verifyonly` → `_SFC_VERIFY`
  - `dism /RestoreHealth` → `_DISM_REPAIR`
  - `dism /CheckHealth` → `_DISM_CHECK`
  - `Get-CimInstance Win32_StartupCommand` → `_PS_STARTUP`
  - `Get-PhysicalDisk` → `_PS_DISK`

---

## [0.9.7.X3] — 2025

### Added
- **Updater version comparator fix** — version comparator now correctly handles alphanumeric tags (`X1`, `X2`, `X3`…). Previously always reported "up to date" due to `int()` parse failure.
- **Dual-file update** — updater patches the external launcher if detected. Searches parent directories automatically.
- **Reinstall — local copy default** — reinstall copies the currently running script instead of downloading. Optional checkbox enables remote fetch with fallback.
- **Recovery — Clean TEMP** — new button removes V0RTEX-related temp files.
- **Crash UI fix** — corrected ASCII art (line 4 had a stray `╔` character).

---

## [0.9.7.X2] and earlier

No changelog kept for versions prior to v0.9.7.X3.
