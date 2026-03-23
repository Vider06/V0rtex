# Changelog — V0RTEX

All notable changes are documented here.  
Format: `[version] — date — summary`

For the full per-version changelog with all technical details, see the release branch:  
[Windows_Release → CHANGELOG.md](https://github.com/Vider06/V0rtex/blob/Windows_Release/CHANGELOG.md)

---

## [1.0.0.X0] — 2026-03-23

### Added

#### 🔐 CRYPT — New Main Tab
A fully dedicated cryptography and hash workstation, added as a standalone top-level tab:
- **ENCRYPT** — AES-256-GCM, RSA, and symmetric key encryption with file or text input
- **DECRYPT** — decrypt output from any supported algorithm
- **INSPECT** — detect encryption type, analyze ciphertext structure, identify algorithm markers
- **HASH** — compute and compare MD5, SHA-1, SHA-256, SHA-512, SHA-3, BLAKE2 for any file or string
- **VIGENÈRE** — classic polyalphabetic cipher encoder/decoder with key analysis

#### 🌐 NET — 6 New Sub-tabs
- **PING / TRACEROUTE** — ICMP ping and network path trace via system command; configurable target, packet count, and timeout
- **PROXY MANAGER** — configure HTTP, HTTPS or SOCKS5 proxy that applies to all V0RTEX network requests; test connectivity and save to config
- **TOR ANONYMOUS ROUTING** — route all V0RTEX traffic through the Tor network; requires Tor installed (auto-detected); toggle per-session or persist to config
- **DNS TRAFFIC NOISE GENERATOR** — generate background DNS queries to mask real traffic patterns; configurable query rate, domain list, and randomization
- **LIVE TRAFFIC MONITOR** — real-time packet capture and display via tshark; filter by protocol, IP, or port; requires tshark installed
- **CONNECTION QUALITY STATS** — track latency, DNS response times and detect network degradation over time; per-target history chart

#### 🎯 IOC — 3 New Sub-tabs
- **IMPHASH** — compute PE import hash (imphash) for malware family clustering and similarity detection; requires pefile; bulk-compare multiple files
- **IOC STATS** — aggregated IOC counts by type across the scan database and recent log files; breakdown chart by IP, domain, hash, URL, email, CVE
- **IOC EXPORT** — scan logs and database, collect all IOCs and export to CSV, JSON, or plain TXT with deduplication and type filtering

#### 🔒 PROT — System Check Enhancement
- **🧬 FULL DEEP SCAN** — new sub-tab inside System Check; extended scan covering all 6 standard health checks plus additional heuristic analysis; longer runtime, more detailed output

#### 👁 WATCHDOG — Restored as Standalone Tab
- Watchdog (folder monitor with real-time change alerts) restored as a top-level tab (`👁 WD`) after being nested inside PROT → System Check in v0.9.8.X2

#### 🔎 LOOK — New Sub-tab
- **FUZZY HASH / SIMILARITY** — compute rolling fuzzy hashes (ssdeep-style, no extra dependencies) and similarity score between two files; useful for detecting variants of the same sample

#### ⚙ CFG — New Sub-tab
- **UPDATE LOG** — browse and inspect past update log files directly from inside the app; shows adapter output, version transitions, and error traces per update session

### Fixed
- **`_detect_platform_branch()`** — now returns the correct release branch per platform (`Windows_Release` / `MacOS_Release` / `Linux_release`) instead of the hardcoded development value `TESTING-GENERAL`
- **`_REMOTE_SCRIPT_NAME`** — simplified to `"v0rtex.py"` unconditionally
- **Reinstall script — `NameError: name '_PLATFORM_BRANCH' is not defined`** — the generated `v0rtex_reinstall.py` now resolves the platform branch inline at runtime instead of relying on the parent scope variable

---

## [0.9.9.X0] — 2026-03-17

### Added
- Centralized versioning system — `_vx_load_ver()` reads `.vx_meta/vx_version` (JSON) at startup and exposes `_VX_VER`, `_VX_NAME`, `_VX_AUTH`, `_VX_FULL`, `_VX_DIRNAME`, `_VX_TITLE`. Fallback assembles the version string at runtime from split fragments. All version literals replaced with variables.
- Settings → ⚡ PERFORMANCE sub-tab — throttle toggle, max background workers, chunk size slider, scan thread delay, niceness slider, cross-link to Advanced
- Recovery UI → 🏷 VERSION tab — reads `.vx_meta/vx_version` independently, shows backup history, dynamic rollback picker, Open Updater button
- Recovery UI — animated rectangle during REPAIR, INSTALL PACKAGES and INTEGRITY CHECK; `✓` for 2.5 s then idle pulse on stop
- Recovery UI — LOG tab saves persistently to `debug_log/recovery_ops/recovery_YYYYMMDD_HHMM.log`
- Recovery UI — PRIMARY ACTIONS section with clean button row in REPAIR tab
- Standalone `v0rtex_updater.py` rewritten — Check GitHub, Download & Update, Rebuild Filesystem, Launch V0RTEX
- Standalone `v0rtex_recovery_ui.py` rewritten — REPAIR and LAUNCH tabs; sentinel + main script detection; self-contained fallback UI
- Background performance helpers `_bg_nice()` and `_bg_scan_delay()` — applied to `_create_full_backup`, `_startup_compile`, `_defense_scan_folder`, `_dsc_run`
- Crash code 106 `VERSION_MISSING`
- `debug_log/recovery_ops/` directory created at startup and by setup wizard

### Changed
- "INSTALLATION MEDIA" → "V0RTEX UTILS" in Recovery UI
- "Keep admin privileges on startup" option removed from Settings
- Admin required popup — navigates to Settings → Advanced → Startup Privileges instead of UAC elevation
- Splash screen overflow fix — `prog_f` `padx` 20 → 12

### Fixed
- Full Scan (DSC) buttons not visible
- System Fixer buttons not visible
- Recovery UI REPAIR layout
- Recovery UI animation stopping correctly
- Standalone updater `_detect_local()` skipping `_ADM_BADGE_*` markers

### Removed
- Internal melt/self-destruct subsystem removed entirely

---

## [0.9.8.X2] — 2026-03-15

### Added
- System Verifier — 6-step Windows health check (Defender, SFC, DISM, SMART, startup persistence); split-pane UI; stall detection; auto-prompt to System Fixer
- System Fixer — Full Repair / SFC Only / DISM Only; SFC output decoded from UTF-16 LE
- YARA multi-engine install chain — yara-python-wheel → yara-x → VS Build Tools + yara-python
- YARA compatibility shim — yara-x wrapped to expose full yara-python API
- tshark auto-resolve at runtime — config, `shutil.which`, registry, known paths
- Update UI — step 7/7 mandatory dep reinstall

### Changed
- YARA removed from `requirements.txt` — handled by install chain only
- Watchdog moved to PROT → System Check sub-tab
- Report Builder tab removed from CFG
- All source comments removed
- All user-facing strings translated to English

### Fixed
- System Fixer progress bar mode
- System Fixer SFC UTF-16 LE output
- YARA MessageBox from background thread
- tshark path not saved to config

### Security
- AV false-positive reduction — sensitive strings assembled at runtime from fragments

---

## [0.9.7.X3] — 2025

### Added
- Updater version comparator — correctly handles alphanumeric tags (`X1`, `X2`, `X3`…)
- Dual-file update — external launcher patched automatically
- Reinstall defaults to local copy
- Recovery UI → Clean TEMP button
- Crash UI ASCII art fix

---

## [0.9.7.X2] and earlier

No changelog kept for versions prior to v0.9.7.X3.
