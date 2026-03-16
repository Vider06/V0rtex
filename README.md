# V0RTEX v0.9.8.X2

**V0RTEX** is a self-contained Windows malware analysis platform built entirely in Python + Tkinter.  
One file. No external launcher. No installer required beyond running `python v0rtex.py`.

> `V = Vider · 0 = zero-day · R = Reverse · T = Threat · E = Engine · X = eXamine`

**Author:** Vider_06  
**Platform:** Windows 10 / 11 (64-bit) only  
**Python:** 3.10 or higher — including 3.12, 3.13, 3.14  
**License:** Copyright © 2024–2026 Vider_06 — All rights reserved. See [LICENSE](./LICENSE).

---

## Index

- [What is V0RTEX?](#what-is-v0rtex)
- [Features at a Glance](#features-at-a-glance)
- [Requirements](#requirements)
- [Installation](#installation)
  - [1. Clone or download](#1-clone-or-download)
  - [2. Run](#2-run)
  - [3. Setup Wizard](#3-setup-wizard)
  - [4. Configure API keys](#4-configure-api-keys)
  - [5. Download YARA rules](#5-download-yara-rules-optional-but-recommended)
- [Folder Structure](#folder-structure)
- [Tab Reference](#tab-reference)
  - [🏠 HOME](#-home)
  - [📋 LOGS](#-logs)
  - [📊 CHRT — Charts](#-chrt--charts)
  - [📁 REP — Reports](#-rep--reports)
  - [🎯 IOC](#-ioc)
  - [🛡 YARA](#-yara)
  - [⚡ PERF](#-perf)
  - [⏱ TL — Timeline](#-tl--timeline)
  - [🔬 SB — Sandbox](#-sb--sandbox)
  - [🏗 SETUP](#-setup)
  - [⚙ CFG — Configuration](#-cfg--configuration)
  - [🔎 LOOK — Lookup](#-look--lookup)
  - [🖥 PROC — Processes](#-proc--processes)
  - [🌐 NET — Network](#-net--network)
  - [📝 NOTES](#-notes)
  - [⚙ SET — Global Settings](#-set--global-settings)
  - [🔒 PROT — App Protection](#-prot--app-protection)
  - [System Check](#system-check-prot--system-check)
  - [System Fixer](#system-fixer)
- [Supported APIs](#supported-apis)
- [Security Notes](#security-notes)
- [Crash Recovery](#crash-recovery)
- [Updating](#updating)
- [Version Scheme](#version-scheme)
- [Contributing](#contributing)
- [License](#license)

---

## What is V0RTEX?

V0RTEX is a complete malware analysis lab that lives inside a single Python script (~29,000 lines). It covers the full analysis workflow: from initial triage and static analysis (hashes, PE headers, strings, entropy, YARA) through dynamic monitoring (process tree, network connections, PCAP capture, sandbox) to post-analysis reporting (HTML/JSON/PDF exports, SQLite history, MITRE ATT&CK mapping). It also includes a self-protection layer, an auto-updater, and a full Windows system health checker — all built directly into the UI with no external tools required beyond Python.

---

## Features at a Glance

| Area | Details |
|------|---------|
| **YARA** | Custom rule editor · Community library downloader · String deobfuscator · Sigma rule viewer · yara-python / yara-x multi-engine |
| **VirusTotal** | File scan · Hash lookup · Bulk batch · Auto-upload · Rescan scheduling |
| **PE Inspector** | Headers · Imports · Exports · Sections · Suspicious API detection · Per-section entropy |
| **IOC** | Auto-extraction (IPs, domains, URLs, hashes, emails, CVEs, registry keys, Win APIs) · MITRE ATT&CK mapping · Feed import · IP/Domain reputation |
| **Sandbox** | Auto-scan watched folder · Process monitor · File analyzer · String extraction · Cuckoo/CAPE integration |
| **Network** | Live connections · PCAP capture (tshark) · Port scan · DNS · WHOIS · SSL/TLS · HTTP headers · URL tools |
| **Crypto / Encoding** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Vigenère · Base64/Hex/XOR · JWT decoder · Hash inspector · ROT |
| **Threat APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan · AlienVault OTX · Shodan · GreyNoise · HybridAnalysis |
| **Entropy** | File entropy chart · Section-level analysis · Verdict gauge |
| **Process** | Live scanner · Service viewer · Startup items · Env variables · Open handles · Process tree |
| **Lookup** | Quick/Bulk hash · Strings · Diff · IOC extract · Regex · Archive · Macro · Bin pattern · Unicode · PE header |
| **Notes** | Scratchpad · MITRE map · TODO list · Snippet library |
| **Defense** | Real-time watchdog · Quarantine · Self-defense · App integrity · Folder protection · Auto-backup |
| **System Check** | Defender status · Quick malware scan · SFC file integrity · DISM image health · Disk SMART · Startup persistence · System Fixer |
| **DB** | SQLite · Full scan history · Export CSV/JSON/HTML · Scan history browser |
| **Updater** | Auto-update check · In-app updater · Dual-file update (external launcher support) · Full dep reinstall on update |

**21 main tabs · 80+ sub-tabs**

---

## Requirements

- Windows 10 or 11 (64-bit)
- Python 3.10 or higher → [python.org](https://www.python.org/downloads/)
- Internet connection (for setup, API lookups, YARA library download)
- Administrator rights — recommended for full functionality (process monitoring, network capture, SFC/DISM)

---

## Installation

### 1. Clone or download

```
git clone https://github.com/Vider06/V0rtex.git
cd V0rtex
```

Or download `v0rtex.py` directly from the [Releases](https://github.com/Vider06/V0rtex/releases) page.

### 2. Run

```
python v0rtex.py
```

> On first launch, V0RTEX detects that it hasn't been installed yet and opens the **Setup Wizard** automatically.

### 3. Setup Wizard

The setup wizard handles everything automatically:

- Installs all Python dependencies via `pip` (bulk install + per-package fallback with 3 strategies + trusted hosts)
- Installs YARA using the multi-engine chain:
  1. `yara-python-wheel` — precompiled wheel, no compiler needed
  2. `yara-x` — Rust-based, no compiler needed, full API shim
  3. VS Build Tools + `yara-python` from source — last resort, shown only after user confirmation
- Auto-detects and optionally installs Wireshark/tshark (checks registry, known paths, `shutil.which`)
- Creates the full folder structure under `V0rtex_System/`
- Writes `config.json`, `whitelist.txt`, `notes.txt` with factory defaults
- Creates `scan_history.db` (SQLite)
- Adds Windows Defender exclusions for the install folder

### 4. Configure API keys

Go to **CFG** tab → **API KEYS** and enter your keys for:
- VirusTotal, MalwareBazaar, AbuseIPDB, URLScan, AlienVault OTX, Shodan, GreyNoise, HybridAnalysis

Keys are stored locally in `config.json`. None are required to use V0RTEX — they only unlock cloud lookup features.

### 5. Download YARA rules (optional but recommended)

Go to **YARA** tab → **LIBRARY** → select the rule repositories you want (Neo23x0, Elastic, Avast, JPCERT/CC, VirusTotal, Yara-Rules, mikesxrs) → click **DOWNLOAD**.

---

## Folder Structure

```
V0rtex_System/
├── V0RTEX_v0.9.8.X2/               ← main install directory
│   ├── v0rtex.py                   ← the entire application (single file)
│   ├── config.json                 ← all user settings and API keys
│   ├── scan_history.db             ← SQLite scan database
│   ├── whitelist.txt               ← SHA-256 hash exclusions
│   ├── notes.txt                   ← persistent scratchpad
│   ├── rules_state.json            ← YARA library download state
│   ├── launch.bat                  ← quick launch script
│   ├── requirements.txt            ← pip dependencies
│   ├── rules/                      ← YARA rule files (.yar / .yara)
│   │   └── external/               ← community rule sets
│   ├── reports/                    ← generated HTML/JSON reports
│   ├── reports_pdf/                ← generated PDF reports
│   ├── modules/                    ← embedded helper modules
│   │   ├── pe_analysis.py
│   │   ├── cuckoo_api.py
│   │   ├── secret_scanner.py
│   │   ├── wireshark.py
│   │   └── __init__.py
│   ├── debug_log/                  ← session logs and crash reports
│   ├── quarantine/                 ← isolated files
│   ├── backups/                    ← auto-created backup ZIPs
│   ├── _recovery/                  ← recovery system working directory
│   ├── sandbox_env/
│   │   └── drop/                   ← auto-scan drop folder
│   ├── threat_feeds/               ← imported threat feed files
│   ├── pcap_dumps/                 ← packet capture output
│   └── diff_workspace/             ← file diff temporary workspace
├── installation_media/
│   ├── v0rtex_reinstall.py         ← reinstall wizard (auto-generated)
│   ├── v0rtex_uninstall.py         ← uninstall wizard (auto-generated)
│   ├── debug_log/                  ← installer logs
│   └── backups/                    ← pre-reinstall/uninstall backups
└── V0rtex_backups/                 ← backup ZIPs (outside V0rtex_System)
```

---

## Tab Reference

### 🏠 HOME
The main dashboard. Displays live scan counters (total, malicious, clean, YARA hits, queue, active APIs), a threat level bar, and a recent scans table. Quick Actions panel: Add File, Add Folder, Scan URL, Sandbox, AutoScan, Watch Folder. Clicking any row in the scan table opens the full scan report popup.

### 📋 LOGS
Two live log panels: **FILE OPERATIONS** (every scan with verdict and timing) and **DEBUG LOG** (internal checkpoints, background thread activity, errors). Logs are mirrored to `debug_log/` on disk. Supports clear and export to `.txt`.

### 📊 CHRT — Charts
Three sub-tabs:
- **Charts** — live bar/pie charts of scan results, updated after each scan.
- **ENT** — entropy distribution histogram across all scanned files.
- **HEAT** — heatmap of threat categories vs file types.

### 📁 REP — Reports
Browse, open and delete scan reports. Supports HTML, JSON and plain text. Side-by-side diff view for comparing two reports.

### 🎯 IOC
- **IOC** — auto-extracts IPs, domains, URLs, hashes, emails, CVEs, registry keys, Windows API names from any file.
- **EXTRACT** — targeted extraction with regex filtering.
- **MITRE** — maps IOCs to MITRE ATT&CK techniques.
- **Feed** — import external threat feed files (CSV, JSON, TXT).
- **Reputation** — bulk IP/domain reputation via configured APIs.
- **Secrets** — detects API keys, tokens, credentials embedded in files.

### 🛡 YARA
- **YARA** — run YARA rules against any file, view hits with rule name, namespace and matched strings.
- **LIBRARY** — download community rule sets from GitHub. Tracks download state per repo.
- **RULE EDITOR** — full YARA authoring with syntax highlighting, compile & test, and test-on-file.
- **DEOBF** — deobfuscation tool: XOR brute-force, Base64, ROT, hex decode.
- **SIGMA** — load and view Sigma `.yml` detection rules.

### ⚡ PERF
System performance monitor: CPU%, RAM, disk I/O, network I/O, per-process breakdown. Refreshes every 5 seconds using a background thread.

### ⏱ TL — Timeline
Chronological scan history chart plotted by verdict, file type and entropy over time.

### 🔬 SB — Sandbox
- **Auto-Scan** — folder watcher with automatic scan queue. Drop a file in `sandbox_env/drop/` and it gets scanned automatically.
- **Process** — live process list with right-click scan/kill/inspect.
- **File Analyzer** — deep static analysis: magic bytes, entropy, PE info, strings, IOC extraction, YARA.
- **Cuckoo/CAPE** — submit to and retrieve results from a local Cuckoo or CAPE instance.

### 🏗 SETUP
The setup and reinstall wizard, accessible without restarting. Lets you reinstall dependencies, reconfigure paths, or fully reinstall V0RTEX in place.

### ⚙ CFG — Configuration
Sub-tabs:
- **API KEYS** — enter and manage API keys for all supported services.
- **CONFIGURATION** — tshark path, proxy settings, request delay, auto-update toggle.
- **WHITELIST** — SHA-256 hash exclusions for scan suppression.
- **EXPORT** — export config, scan history and notes.
- **CHECKPOINT** — save and restore named snapshots of the full app state.
- **SCAN HISTORY** — full SQLite browser with filter, search and export.
- **DEBUG LOG** — browse and open debug log files.
- **UPDATER** — check for updates, configure auto-check, view update history.

### 🔎 LOOK — Lookup
Hash · HEX viewer · REGEX tester · DOC inspector · SIG (signature) viewer · BATCH scanner · DIFF (side-by-side file diff) · ARCHIV (archive inspector) · MACRO (Office macro extractor) · B64 (Base64 encode/decode) · XOR (XOR brute-force) · BCONV (binary/hex converter) · JWT decoder · ROT cipher · PE-HDR (PE header dump) · UNICODE (string normalizer) · BINPAT (binary pattern search)

### 🖥 PROC — Processes
- **Processes** — live process list with PID, name, CPU, RAM, path.
- **Services** — Windows services browser with start/stop controls.
- **Startup Items** — lists all `Win32_StartupCommand` entries.
- **Env Variables** — full environment variable dump.
- **Handles** — open file/registry handles per process.
- **Proc Tree** — visual process hierarchy.
- **Registry** — registry key browser with search.

### 🌐 NET — Network
- **Connections** — live TCP/UDP connections with remote IP, port and process.
- **URL Tools** — URL encode/decode, expand shortened URLs.
- **IP/Domain Rep.** — bulk reputation lookup.
- **DNS** — DNS record lookup (A, AAAA, MX, TXT, NS, CNAME).
- **WHOIS** — full WHOIS data for IPs and domains.
- **HTTP Headers** — raw HTTP header inspector.
- **SSL/TLS** — certificate chain viewer.
- **Port Scan** — TCP port scanner with configurable range.
- **PCAP** — start/stop tshark capture, open in Wireshark.

### 📝 NOTES
- **Notepad** — persistent scratchpad saved to `notes.txt`.
- **MITRE ATT&CK** — searchable technique reference.
- **TODO** — task list with checkboxes, saved to `todo_list.json`.
- **Snippets** — code/IOC snippet library saved to `snippets.json`.

### ⚙ SET — Global Settings
Interface · Scan · Privacy · Paths · Network · Defense · Notifications · Advanced · Automatic Actions

### 🔒 PROT — App Protection
- **Build/Destroy** — set up and tear down the protected environment.
- **Protected Folders** — monitor folders for unauthorized changes.
- **Integrity** — hash-based verification of all V0RTEX files.
- **Defense** — real-time defense engine with auto-quarantine.
- **Self-Defense** — process-level protection against termination.
- **Backup** — create and restore full lab ZIP backups.
- **System Check** — 6-step Windows health scan (see below).
- **Watchdog** — file system watcher with configurable alerts.

#### System Check (PROT → System Check)
A full Windows health scan that runs entirely inside V0RTEX without opening any external tools:

| Step | Check | Tool used |
|------|-------|-----------|
| 1 | Windows Defender / AV status | `Get-MpComputerStatus` |
| 2 | Quick malware scan + active threat list | `Start-MpScan` + `Get-MpThreat` |
| 3 | System file integrity | `sfc /verifyonly` (direct, not via PowerShell pipe) |
| 4 | Windows image health | `dism /CheckHealth` (admin only) |
| 5 | Disk SMART status | `Get-PhysicalDisk` |
| 6 | Startup persistence | `Win32_StartupCommand` + suspicious keyword detection |

Split-pane UI: **SCAN LOG** on the left (human-readable results), **RAW TERMINAL OUTPUT** on the right (exact command + `[ADMIN]`/`[no admin]` tag). Spinner + elapsed time + stall warning if a step hangs. Auto-prompts **System Fixer** on issues.

#### System Fixer
Standalone repair window accessible from System Check:
- **Full Repair** — threat removal → SFC (`sfc /scannow`) → DISM (`dism /RestoreHealth`) in sequence.
- **SFC Only** — run SFC independently.
- **DISM Only** — run DISM independently.
Progress bar uses `indeterminate` mode during long operations (SFC/DISM give no percentage output).

---

## Supported APIs

V0RTEX integrates with the following external services. All are optional — no key is required to use local analysis features.

| Service | Used for |
|---------|---------|
| VirusTotal | File scan, hash lookup, bulk batch, URL scan |
| MalwareBazaar | Hash lookup, sample download |
| AbuseIPDB | IP reputation |
| URLScan.io | URL analysis |
| AlienVault OTX | IOC reputation, pulses |
| Shodan | Host info, open ports |
| GreyNoise | IP noise classification |
| HybridAnalysis | Sandbox submission and results |

---

## Security Notes

V0RTEX requires administrator rights for some features (System Check/Fixer, Defender interaction, process monitoring). It will work with limited rights, but some tabs will be restricted.

Sensitive PowerShell/system commands are assembled at runtime from string fragments rather than stored as literals in the source. This reduces false positives from antivirus engines that flag static string patterns.

If Windows Defender flags V0RTEX, add the install folder to your Defender exclusion list. The setup wizard does this automatically.

---

## Crash Recovery

If V0RTEX crashes on startup or mid-session, a **Recovery Terminal** launches automatically. From there you can:
- View the crash report and session log
- Clean TEMP files
- Reinstall dependencies
- Roll back to a previous backup
- Perform a full reinstall

Crash reports are saved to `debug_log/` with timestamps.

---

## Updating

V0RTEX has a built-in updater (CFG → UPDATER). When an update is available:
1. Downloads the new `v0rtex.py` from GitHub
2. Creates a timestamped backup ZIP of your current install (config, rules, reports, DB)
3. Applies the update
4. If you run V0RTEX from an external launcher outside `V0rtex_System/`, the updater auto-detects and updates that file too
5. Reinstalls all dependencies using the multi-strategy pipeline

Auto-update check can be toggled in CFG → CONFIGURATION.

---

## Version Scheme

```
MAJOR . BIG_UPDATE . SMALL_UPDATE . X[BUGFIX]

Example: 0.9.8.X2
  0       = major version
  9       = big update (significant feature batch)
  8       = small update (incremental features)
  X2      = second bugfix release on top of 0.9.8
```

---

## Contributing

Issues and pull requests are welcome. If you find a bug, open an issue with:
- V0RTEX version (shown in the bottom status bar)
- Python version (`python --version`)
- Windows version
- The contents of the relevant crash report from `debug_log/`

---

## License

Copyright © 2024–2026 Vider_06. All rights reserved.  
See [LICENSE](./LICENSE) for full terms.
