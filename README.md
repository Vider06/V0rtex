# V0RTEX v0.9.8.X1

**V0RTEX** is a self-contained Windows malware analysis platform built in Python + Tkinter.  
`V = Vider · 0 = zero-day · R = Reverse · T = Threat · E = Engine · X = eXamine`

> **Author:** Vider_06  
> **Platform:** Windows 10/11 only · Python 3.10+ (Python 3.14 supported) · Single file, no external launcher required  
> **License:** Copyright © 2024-2025 Vider_06 — All rights reserved. See [LICENSE](./LICENSE).

---

## Features at a glance

| Area | Details |
|------|---------|
| **YARA** | Custom rule editor · Community library downloader · String deobfuscator · Sigma rule viewer |
| **VirusTotal** | File scan · Hash lookup · Bulk batch · Auto-upload · Rescan scheduling |
| **PE Inspector** | Headers · Imports · Exports · Sections · Suspicious API detection · Per-section entropy |
| **IOC** | Auto-extraction · MITRE ATT&CK mapping · Feed import · IP/Domain reputation |
| **Sandbox** | Auto-scan watched folder · Process monitor · File analyzer · String extraction · Cuckoo/CAPE |
| **Network** | Live connections · PCAP capture · Port scan · DNS · WHOIS · SSL/TLS · HTTP headers · URL tools |
| **Crypto** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Vigenère · Base64/Hex/XOR · JWT decoder · Hash inspector |
| **APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan · AlienVault OTX · Shodan · GreyNoise · HybridAnalysis |
| **Entropy** | File entropy chart · Section-level analysis · Verdict gauge |
| **Process** | Live scanner · Service viewer · Startup items · Env variables · Open handles · Process tree |
| **Lookup** | Quick/Bulk hash · Strings · Diff · IOC extract · Regex · Archive · Macro · Bin pattern · Unicode · PE header |
| **Notes** | Scratchpad · MITRE map · TODO list · Snippet library |
| **Defense** | Real-time watchdog · Quarantine · Self-defense · App integrity · Folder protection · Auto-backup |
| **DB** | SQLite · Full scan history · Export CSV/JSON/HTML · Scan history browser |
| **System Check** | SFC scan · DISM health check · Defender status · Disk SMART · Startup persistence · System Fixer |

**21 main tabs · 80+ sub-tabs**

---

## What's new in v0.9.8.X1

See [CHANGELOG.md](./CHANGELOG.md) for the full list of changes.

**Highlights:**
- **System Verifier** — new PROT → System Check tab runs a 6-step Windows health scan entirely inside V0RTEX: Defender status, quick malware scan, SFC file integrity, DISM image health, disk SMART, startup persistence check. Raw PS commands shown in terminal panel with `[ADMIN]`/`[no admin]` tag. Auto-prompts **System Fixer** on issues.
- **System Fixer** — repair window with Full Repair (threat removal → SFC → DISM), SFC Only, DISM Only. Progress bar uses `indeterminate` animation during long operations.
- **YARA engine auto-detection** — installer tries `yara-python-wheel` → `yara-x` (Rust, no compiler needed) → VS Build Tools as last resort with full user confirmation popup
- **Python 3.12+ support** — `yara-python` no longer required; `yara-x` compatibility shim exposes identical API (`yara.compile`, `rules.match`, `yara.SyntaxError`)
- **AV false-positive reduction** — all sensitive string literals assembled at runtime from split fragments
- **tshark auto-resolve** — runtime auto-detects Wireshark via registry, known paths and `shutil.which`
- **Update UI — mandatory dep reinstall** — every update now includes step 7/7 that reinstalls all dependencies
- **All comments removed** — source is comment-free; all user-facing strings in English

---

## Installation

### Requirements
- Windows 10 or 11 (64-bit)
- Python 3.10 or higher (including 3.12, 3.13, 3.14) → [python.org](https://www.python.org/downloads/)
- Internet connection
- Administrator rights recommended for first launch

### Steps

1. **Clone or download** this repository:
```
git clone https://github.com/Vider06/V0rtex.git
```

2. **Run the file:**
```
python v0rtex.py
```

3. **Follow the setup wizard** — it automatically:
   - Installs all Python packages via `pip`
   - Installs YARA: tries `yara-python-wheel` → `yara-x` → VS Build Tools (with confirmation popup)
   - Downloads and installs Wireshark/tshark (optional)
   - Creates the full folder structure
   - Writes `config.json`, `whitelist.txt`, `notes.txt` with factory defaults
   - Creates `scan_history.db`
   - Adds Windows Defender exclusions for the install folder

4. **Configure API keys** → `CFG` tab → `API KEYS`

5. **Download YARA rules** → `YARA` tab → `LIBRARY` → select repos → **DOWNLOAD**

> ⚠ **Run as Administrator** on first launch for full process/network monitoring.

---

## Folder Structure
```
V0rtex_System/
├── V0RTEX_v0.9.8.X1/               ← main install directory (BASE_DIR)
│   ├── v0rtex.py                   ← the entire application
│   ├── config.json                 ← all user settings
│   ├── scan_history.db             ← SQLite database
│   ├── whitelist.txt               ← hash/path exclusions
│   ├── notes.txt                   ← scratchpad persistent storage
│   ├── rules_state.json            ← YARA library download state
│   ├── launch.bat                  ← quick launch script
│   ├── requirements.txt            ← pip requirements
│   ├── rules/                      ← YARA rule files (.yar / .yara)
│   │   └── external/               ← community rule sets
│   ├── reports/                    ← generated HTML/PDF/JSON reports
│   ├── reports_pdf/                ← generated PDF reports
│   ├── modules/                    ← embedded helper modules
│   │   ├── pe_analysis.py
│   │   ├── cuckoo_api.py
│   │   ├── secret_scanner.py
│   │   ├── wireshark.py
│   │   └── __init__.py
│   ├── debug_log/                  ← session logs and crash reports
│   ├── quarantine/                 ← isolated malicious files
│   ├── backups/                    ← auto-created backup ZIPs
│   ├── _recovery/                  ← recovery system working directory
│   ├── sandbox_env/                ← sandbox working environment
│   │   └── drop/                   ← auto-scan drop folder
│   ├── threat_feeds/               ← imported threat feed files
│   ├── pcap_dumps/                 ← packet capture files
│   └── diff_workspace/             ← file diff temporary workspace
├── installation_media/
│   ├── v0rtex_reinstall.py         ← reinstall wizard (generated)
│   ├── v0rtex_uninstall.py         ← uninstall wizard (generated)
│   ├── debug_log/                  ← installer session logs
│   └── backups/                    ← pre-uninstall/reinstall backups
└── V0rtex_backups/                 ← backup ZIPs (outside V0rtex_System)
```

---

## Main UI — Tab Reference

### 🏠 HOME
The main dashboard. Shows live scan statistics (total scans, malicious, clean, YARA hits, queue, API keys), a threat level bar, and the recent scans table. The right panel contains **Quick Actions** (Add File, Add Folder, Scan URL, Sandbox, AutoScan, Watch Folder) and **V0RTEX INFO** (build info, version, APIs). Clicking any row in the recent scans table opens the full scan report popup.

### 📋 LOGS
Three log panels in a scrollable view: **FILE OPERATIONS** (every scan event with verdict), **DEBUG LOG** (internal checkpoints, errors, background thread activity). Logs are also written to `debug_log/` on disk. A clear button and export to `.txt` are available.

### 📊 CHRT (Charts)
Three sub-tabs:
- **Charts** — live bar/pie charts of scan results (malicious vs clean vs YARA), updated after each scan.
- **ENT** — entropy distribution histogram across all scanned files.
- **HEAT** — heatmap of threat categories vs file types across all scanned samples.

### 📁 REP (Reports)
Browse, open and delete scan reports. Supports HTML, JSON and plain text formats. Diff view compares two reports side by side.

### 🎯 IOC
- **IOC** — automatic extraction of IPs, domains, URLs, hashes, email addresses, CVEs, registry keys and Windows API names.
- **MITRE** — maps extracted IOCs to MITRE ATT&CK techniques.
- **Feed** — import external threat feed files (CSV, JSON, TXT).
- **IP/Domain Rep. · Stats · Export** — bulk reputation lookup and IOC export.

### 🛡 YARA
- **YARA** — run YARA against any file, view hits with rule name, namespace and matched strings.
- **LIBRARY** — download community rule sets from GitHub (Neo23x0, Elastic, Avast, VirusTotal, Yara-Rules, JPCERT/CC, mikesxrs).
- **✏ RULE EDITOR** — full YARA rule authoring with syntax highlighting. Compile & Test + Test on File.
- **DEOBF** — string deobfuscator: XOR brute-force, base64, ROT, hex.
- **Σ SIGMA** — load Sigma `.yml` detection rules.

### ⚡ PERF
System performance monitor. CPU%, RAM, disk I/O, network I/O, per-process breakdown. Updates every 5 seconds.

### ⏱ TL (Timeline)
Chronological scan history chart plotted by verdict, file type and entropy.

### 🔬 SB (Sandbox)
- **Auto-Scan** — folder watcher with automatic queue.
- **Process** — live process list with right-click scan/kill.
- **File Analyzer** — deep static analysis: magic bytes, entropy, PE info, strings, IOCs, YARA.
- **String Extract** — ASCII and Unicode string extraction with configurable minimum length.

### 🏗 SETUP
Setup and reinstall wizard accessible from the main UI.

### ⚙ CFG (Config)
API KEYS · CONFIGURATION · WHITELIST · EXPORT · CHECKPOINT · SCAN HISTORY · DEBUG LOG · UPDATER

### 🔎 LOOK (Lookup)
Hash · HEX · REGEX · DOC · SIG · BATCH · DIFF · ARCHIV · MACRO · B64 · XOR · BCONV · JWT · ROT · PE-HDR · UNICODE · BINPAT

### 🖥 PROC (Processes)
Processes · Services · Startup Items · Env Variables · Handles · Proc Tree · Registry

### 🌐 NET (Network)
Connections · URL Tools · IP/Domain Rep. · DNS · WHOIS · HTTP Headers · SSL/TLS · Port Scan · PCAP

### 📝 NOTES
Notepad · MITRE ATT&CK · TODO · Snippets

### ⚙ SET (Global Settings)
Interface · Scan · Privacy · Paths · Network · Defense · Notifications · Advanced · Automatic Actions

### 🔒 PROT (App Protection)
Five sub-tabs:
- **Build/Destroy** — protected environment setup.
- **Protected Folders** — monitor folders for unauthorized changes.
- **Integrity** — hash verification of all critical V0RTEX files.
- **Defense** — real-time defense engine.
- **Self-Defense** — process-level protection.
- **Backup** — full lab ZIP backups.
- **🔍 System Check** — three sub-tabs:
  - **SCAN** — Windows system verification: Defender status, quick malware scan, SFC file integrity, DISM image health, disk SMART, startup persistence. Shows raw PowerShell commands in terminal panel with `[ADMIN]`/`[no admin]` tag.
  - **WHITELIST** — exclusions for the startup entry scanner.
  - **👁 WATCHDOG** — folder monitor for new/modified files with auto-queue to scanner.

### 🔐 CRYPT (Crypto)
Encrypt · Decrypt · Inspect · Hash · Vigenère

### ⚠ DZ (Danger Zone)
Destructive and diagnostic tools. Includes clear logs, factory reset, secure wipe, system info.

---

## Recovery UI

V0RTEX has a built-in **Recovery Terminal** that activates automatically when critical files are missing, corrupted or when a crash is detected before the main UI loads.

### When it triggers
- Embedded module files are missing from `BASE_DIR`
- `config.json` is corrupted or has invalid JSON
- `scan_history.db` is missing or has a broken schema
- An unhandled exception occurs before the main window is displayed

### Tabs
| Tab | Description |
|-----|-------------|
| **>_ Terminal** | Embedded command shell with QUICK CMDS panel |
| **💥 Crash Log** | Full traceback from last session |
| **📋 File Check** | Verifies presence of all expected files |
| **🔧 Repair** | Recreate files · Reset config · Repair DB · Install packages · Restore backup · Clean TEMP |
| **💾 Backup** | Create and list backup ZIPs |
| **🩺 Diagnostics** | Dependency check · YARA rules · Processes · Network |
| **🧹 Clean** | Remove orphaned temp files, `__pycache__`, `.pyc` |
| **🌐 Network** | Connectivity test, DNS, proxy, VT API check |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **Window opens and immediately closes** | Run from terminal (`python v0rtex.py`). If Recovery Terminal appears use **Recreate Critical Files** |
| **`KeyError` on startup** | Corrupt `config.json` — Recovery Terminal → Reset config.json |
| **YARA not working / disabled** | Recovery Terminal → Install / Repair Packages. With Python 3.12+, `yara-x` is installed automatically as fallback |
| **VirusTotal returns no results** | CFG → API KEYS — verify key. Free tier: 500 requests/day |
| **tshark / network capture missing** | Install Wireshark from [wireshark.org](https://www.wireshark.org/). V0RTEX will auto-detect it via registry even if not on PATH |
| **Setup crashes with admin error** | Right-click `v0rtex.py` → *Run as administrator* |
| **High memory on startup** | Background YARA compile is running — wait 30–60 seconds |
| **Recovery Terminal appears every launch** | Antivirus deleted module files — add install folder to Defender exclusions (done automatically by setup) |
| **Crash report on every launch** | Check `debug_log/crash_log.txt` and open a GitHub Issue |
| **Updater says "up to date" on old version** | Update to v0.9.8.X1 — earlier versions had a version comparison bug with alphanumeric tags |

---

## Dependencies

Installed automatically by the setup wizard:

```
requests · psutil · pefile · Pillow · cryptography · python-whois
dnspython · matplotlib · tkinterdnd2 · fpdf2 · watchdog · pystray
reportlab · chardet · PyYAML · olefile · numpy
```

**YARA** (installed separately with multi-fallback):
- `yara-python-wheel` — precompiled, no compiler needed *(preferred)*
- `yara-x` — Rust-based, precompiled, full API compatibility shim *(fallback)*
- `yara-python` from source via VS Build Tools *(last resort, requires confirmation)*

**Optional:**
- **Wireshark/tshark** — network capture (prompted during setup, auto-detected at runtime)

---

## License

Copyright © 2024-2025 Vider_06 — All rights reserved.  
Redistribution, resale, and repackaging are strictly prohibited.  
See [LICENSE](./LICENSE) for full terms.

If you are reading this... Why would you EVER read all of this dude  
Alr, try it and report me bugs or anything tbh  
- Vider_06
