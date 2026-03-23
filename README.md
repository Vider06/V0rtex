# V0RTEX

**V0RTEX** is a self-contained Windows malware analysis platform built entirely in Python + Tkinter.  
One file. No external launcher. No installer required beyond running `python v0rtex.py`.

> `V = Vider · 0 = zero-day · R = Reverse · T = Threat · E = Engine · X = eXamine`

**Author:** Vider_06  
**Platform:** Windows 10 / 11 (64-bit)  
**Python:** 3.10 or higher — including 3.12, 3.13, 3.14  
**License:** Copyright © 2024–2026 Vider_06 — All rights reserved. See [LICENSE.txt](LICENSE.txt).

---

## Index

- [What is V0RTEX?](#what-is-v0rtex)
- [Download](#download)
- [Requirements](#requirements)
- [Installation](#installation)
- [Features at a Glance](#features-at-a-glance)
- [Tab Reference](#tab-reference)
- [Supported APIs](#supported-apis)
- [Folder Structure](#folder-structure)
- [Security Notes](#security-notes)
- [Crash Recovery](#crash-recovery)
- [Updating](#updating)
- [Version Scheme](#version-scheme)
- [License](#license)

---

## What is V0RTEX?

V0RTEX is a complete malware analysis lab that lives inside a single Python script (~35,500 lines). It covers the full analysis workflow: from initial triage and static analysis (hashes, PE headers, strings, entropy, YARA) through dynamic monitoring (process tree, network connections, PCAP capture, sandbox) to post-analysis reporting (HTML / JSON / PDF exports, SQLite history, MITRE ATT&CK mapping).

It also includes a dedicated cryptography workstation, a self-protection layer, an auto-updater, a full Windows system health checker, and a standalone Recovery UI — all built directly into the application with no external tools required beyond Python.

**22 main tabs · 80+ sub-tabs**

---

## Download

> This is the main repository branch. It does not contain runnable code.  
> All downloads are on the platform-specific release branches.

### Windows

Latest release: **v1.0.0.X0**

Browse the release branch: [Windows_Release](https://github.com/Vider06/V0rtex/tree/Windows_Release)

Download the zip directly:  
**[⬇ Download V0RTEX for Windows](https://github.com/Vider06/V0rtex/archive/refs/heads/Windows_Release.zip)**

Extract the zip and run:

```
python v0rtex.py
```

On first launch the Setup Wizard opens automatically and handles everything.

---

## Requirements

- Windows 10 or 11 (64-bit)
- [Python 3.10 or higher](https://www.python.org/downloads/) — including 3.12, 3.13, 3.14
- Internet connection — required for setup, API lookups, YARA rule downloads, and updates
- Administrator rights — recommended for full functionality (process monitoring, network capture, SFC/DISM, Defender interaction)

Optional but recommended:
- [Wireshark / tshark](https://www.wireshark.org/) — required for PCAP capture and Live Traffic Monitor
- [Tor](https://www.torproject.org/) — required for anonymous routing via the Tor tab

---

## Installation

### 1. Download

Download the zip from the link above and extract it anywhere you want. The setup wizard will create the full directory structure on its own.

### 2. Run

```
python v0rtex.py
```

On first launch V0RTEX detects it hasn't been installed yet and opens the **Setup Wizard** automatically.

### 3. Setup Wizard

The setup wizard handles everything automatically:

- Installs all Python dependencies via `pip` — bulk install with per-package fallback and 3 strategies per package
- Installs the YARA engine using a multi-strategy chain:
  1. `yara-python-wheel` — precompiled wheel, no compiler needed
  2. `yara-x` — Rust-based, no compiler needed, full API compatibility shim
  3. VS Build Tools + `yara-python` from source — last resort, shown only after user confirmation
- Auto-detects Wireshark/tshark (checks config, `shutil.which`, Windows registry, known install paths)
- Creates the full folder structure under `V0rtex_System/`
- Writes `config.json`, `whitelist.txt`, `notes.txt` with factory defaults
- Creates `scan_history.db` (SQLite)
- Adds Windows Defender exclusions for the install folder and Python processes
- Writes `v0rtex_uninstall.py`, `v0rtex_reinstall.py`, `v0rtex_updater.py`, `v0rtex_recovery_ui.py` to `v0rtex_utils/`

### 4. Configure API keys

Go to **CFG** tab → **API KEYS** and enter your keys for any of the supported services.  
Keys are stored locally in `config.json`. None are required — they only unlock cloud lookup features.

### 5. Download YARA rules (optional but recommended)

Go to **YARA** tab → **LIBRARY** → select the repositories you want (Neo23x0, Elastic, Avast, JPCERT/CC, VirusTotal, Yara-Rules, mikesxrs) → click **DOWNLOAD**.

---

## Features at a Glance

| Area | Details |
|------|---------|
| **YARA** | Custom rule editor · Community library downloader · String deobfuscator · Sigma rule viewer · yara-python / yara-x multi-engine |
| **VirusTotal** | File scan · Hash lookup · Bulk batch · Auto-upload · Rescan scheduling |
| **PE Inspector** | Headers · Imports · Exports · Sections · Suspicious API detection · Per-section entropy |
| **IOC** | Auto-extraction (IPs, domains, URLs, hashes, emails, CVEs, registry keys, Win APIs) · MITRE ATT&CK mapping · Feed import · IP/Domain reputation · Imphash · IOC stats · IOC export |
| **Cryptography** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Vigenère · Base64/Hex/XOR · JWT decoder · Hash inspector · ROT · Fuzzy hash similarity |
| **Sandbox** | Auto-scan watched folder · Process monitor · File analyzer · String extraction · Cuckoo/CAPE integration |
| **Network** | Live connections · PCAP capture · Live traffic monitor · Port scan · Ping/Traceroute · Proxy manager · Tor routing · DNS noise generator · Connection stats · DNS · WHOIS · SSL/TLS · HTTP headers · URL tools |
| **Threat APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan · AlienVault OTX · Shodan · GreyNoise · HybridAnalysis |
| **Entropy** | File entropy chart · Section-level analysis · Verdict gauge |
| **Process** | Live scanner · Service viewer · Startup items · Env variables · Open handles · Process tree · Registry browser |
| **Lookup** | Quick/Bulk hash · Strings · Diff · IOC extract · Regex · Archive · Macro · Bin pattern · Unicode · PE header · Hex viewer · Signature verify · Doc analyzer · Fuzzy hash |
| **Notes** | Scratchpad · MITRE map · TODO list · Snippet library |
| **Defense** | Real-time watchdog · Quarantine · Self-defense · App integrity · Folder protection · Auto-backup |
| **Performance** | Throttle toggle · Max workers · Chunk size · Scan delay · Niceness slider · Background CPU/IO limiters |
| **System Check** | Defender status · Quick malware scan · SFC file integrity · DISM image health · Disk SMART · Startup persistence · Full deep scan · System Fixer |
| **DB** | SQLite · Full scan history · Export CSV/JSON/HTML · Scan history browser |
| **Updater** | Auto-update check · In-app updater · Standalone updater · Dual-file update · Full dep reinstall on update |
| **Recovery** | Standalone Recovery UI · Version tab with rollback · Animated repair · Persistent recovery logs |

---

## Tab Reference

### 🏠 HOME

The main dashboard with three sub-tabs:

- **DASHBOARD** — live scan counters (total, malicious, clean, YARA hits, queue, active APIs), threat level bar, recent scans table with verdict color coding. Quick Actions panel: Add File, Add Folder, Scan URL, Sandbox, AutoScan, Watch Folder. Clicking any row opens the full scan report popup.
- **INFO** — system info, Python version, installed packages, V0RTEX path and version details.
- **README** — the app README rendered inline.

### 📋 LOGS

Two live log panels: **FILE OPERATIONS** (every scan with verdict and timing) and **DEBUG LOG** (internal checkpoints, background thread activity, errors). Logs are mirrored to `debug_log/` on disk. Supports clear and export to `.txt`.

### 📊 CHRT — Charts

- **Charts** — live bar/pie charts of scan results, updated after each scan
- **ENT** — entropy distribution histogram across all scanned files
- **HEAT** — heatmap of threat categories vs file types

### 📁 REP — Reports

Browse, open and delete scan reports. Supports HTML, JSON and plain text. Side-by-side diff view for comparing two reports.

### 🎯 IOC

- **IOC** — auto-extracts IPs, domains, URLs, hashes, emails, CVEs, registry keys, Windows API names from any file
- **EXTRACT** — targeted extraction with regex filtering
- **MITRE** — maps IOCs to MITRE ATT&CK techniques
- **Feed** — import external threat feed files (CSV, JSON, TXT)
- **Reputation** — bulk IP/domain reputation via configured APIs
- **Secrets** — detects API keys, tokens, credentials embedded in files
- **IMPHASH** — compute PE import hash for malware family clustering; bulk-compare multiple PE files
- **IOC STATS** — aggregated IOC counts by type from the scan DB and recent logs; breakdown chart
- **IOC EXPORT** — collect all IOCs from logs and DB and export to CSV, JSON, or TXT with deduplication

### 🛡 YARA

- **YARA** — run YARA rules against any file; view hits with rule name, namespace and matched strings
- **LIBRARY** — download community rule sets from GitHub; tracks download state per repository
- **RULE EDITOR** — full YARA authoring with syntax highlighting, compile & test, and test-on-file
- **DEOBF** — deobfuscation tool: XOR brute-force, Base64, ROT, hex decode
- **SIGMA** — load and view Sigma `.yml` detection rules

### ⚡ PERF

System performance monitor: CPU%, RAM, disk I/O, network I/O, per-process breakdown. Refreshes every 5 seconds via background thread.

### ⏱ TL — Timeline

Chronological scan history chart plotted by verdict, file type and entropy over time.

### 🔬 SB — Sandbox

- **Auto-Scan** — folder watcher with automatic scan queue; drop a file in `sandbox_env/drop/` and it scans automatically
- **Process** — live process list with right-click scan/kill/inspect
- **File Analyzer** — deep static analysis: magic bytes, entropy, PE info, strings, IOC extraction, YARA

### 🐦 Cuckoo/CAPE

Submit files to and retrieve results from a local Cuckoo or CAPE instance.

### 🏗 SETUP

The setup and reinstall wizard, accessible without restarting. Reinstall dependencies, reconfigure paths, or fully reinstall V0RTEX in place.

### ⚙ CFG — Configuration

- **API KEYS** — enter and manage API keys for all supported services with live test buttons
- **CONFIGURATION** — tshark path, proxy settings, request delay, auto-update toggle
- **WHITELIST** — SHA-256 hash exclusions for scan suppression
- **EXPORT** — export config, scan history and notes
- **CHECKPOINT** — save and restore named snapshots of the full app state
- **SCAN HISTORY** — full SQLite browser with filter, search and export (CSV/JSON/HTML)
- **DEBUG LOGS** — browse and open debug log files by category
- **UPDATE LOG** — browse past update session logs; shows adapter output, version transitions, error traces
- **UPDATER** — check for updates, configure auto-check, view update history, trigger manual update

### 🔎 LOOK — Lookup

- **Hash** — quick and bulk hash lookup (MD5, SHA-1, SHA-256, SHA-512) for files and strings
- **HEX** — hex viewer with ASCII panel and offset display
- **REGEX** — regex tester with match highlighting and group breakdown
- **DOC** — Office document analyzer (DOCX, XLSX, PPTX): extract metadata, embedded objects, macros
- **SIG** — signature verify: check Authenticode signatures on PE files
- **BATCH** — bulk hash scanner: hash a folder of files and cross-check against known IOCs
- **DIFF** — side-by-side text/binary diff between two files
- **ARCHIV** — archive inspector: list contents of ZIP, RAR, 7z, TAR without extracting; flag suspicious entries
- **B64** — Base64 encode/decode with auto-detection
- **XOR** — XOR brute-force with key length detection and entropy output
- **BCONV** — binary/hex/decimal/octal converter
- **JWT** — JWT decoder: header, payload, signature; no secret required
- **ROT** — ROT-N cipher with all 25 rotations shown simultaneously
- **PE-HDR** — PE header dump: DOS header, NT headers, section table, import/export directory
- **UNICODE** — Unicode string normalizer and encoding detector
- **BINPAT** — binary pattern search: find byte sequences, magic bytes, or shellcode signatures
- **FUZZY** — fuzzy hash similarity: compute rolling hashes and similarity score between two files (ssdeep-style, no extra dependencies)

### 🖥 PROC — Processes

- **Processes** — live process list with PID, name, CPU%, RAM, path; right-click to scan, kill or inspect
- **Services** — Windows services browser with start/stop/restart controls
- **Startup Items** — lists all `Win32_StartupCommand` entries with path and registry location
- **Env Variables** — full environment variable dump with search
- **Handles** — open file/registry handles per process
- **Proc Tree** — visual process hierarchy tree
- **Registry** — registry key browser with search and value display

### 🌐 NET — Network

- **Connections** — live TCP/UDP connections with remote IP, port, state and process name
- **URL Tools** — URL encode/decode, redirect chain follower, expand shortened URLs
- **IP/Domain Rep.** — bulk reputation lookup via configured APIs
- **DNS** — DNS record lookup (A, AAAA, MX, TXT, NS, CNAME, PTR)
- **WHOIS** — full WHOIS data for IPs and domains
- **HTTP Headers** — raw HTTP response header inspector
- **SSL/TLS** — certificate chain viewer: subject, issuer, validity, SANs, fingerprint
- **Port Scan** — TCP port scanner with configurable range and timeout
- **PCAP** — start/stop tshark capture; open capture in Wireshark; filter by interface and protocol
- **PING / Traceroute** — ICMP ping and network path trace; configurable count and timeout
- **Proxy Manager** — configure HTTP, HTTPS or SOCKS5 proxy; applies to all V0RTEX network requests; test and save
- **Tor** — route all V0RTEX traffic through the Tor network; toggle per-session or persist to config
- **DNS Noise Generator** — generate background DNS queries to mask real traffic patterns; configurable rate and domain list
- **Live Traffic Monitor** — real-time packet capture and display via tshark; filter by protocol, IP, or port
- **Connection Stats** — track latency, DNS response times, and detect network degradation over time

### 📝 NOTES

- **Notepad** — persistent scratchpad saved to `notes.txt`
- **MITRE ATT&CK** — searchable MITRE technique reference with tactic grouping
- **TODO** — task list with checkboxes, priorities, and due dates; saved to `todo_list.json`
- **Snippets** — code/IOC snippet library with tags and search; saved to `snippets.json`

### ⚙ SET — Global Settings

- **Interface** — theme, font size, window behavior
- **Scan** — default scan depth, file size limits, auto-submit toggles
- **Privacy** — log retention, auto-censor, data collection settings
- **Paths** — custom paths for rules, quarantine, reports, backups
- **Network** — timeout, retry, proxy defaults
- **Defense** — auto-quarantine thresholds, watchdog sensitivity
- **Notifications** — desktop notification toggles per event type
- **⚡ Performance** — throttle scan threads toggle, max background workers, chunk size, scan thread delay, niceness slider, cross-link to Advanced
- **Advanced** — startup flags, admin behavior, debug verbosity
- **Automatic Actions** — auto-actions triggered on specific verdicts or events

### 🔒 PROT — App Protection

- **Build/Destroy** — set up and tear down the protected environment
- **Protected Folders** — monitor folders for unauthorized changes; configurable alert actions
- **Integrity** — hash-based verification of all V0RTEX files; detect tampering
- **Defense** — real-time defense engine with auto-quarantine on threshold breach
- **Self-Defense** — process-level protection against external termination
- **Backup** — create and restore full lab ZIP backups with timestamp history
- **System Check** — 6-step Windows health scan:

| Step | Check | Tool |
|------|-------|------|
| 1 | Windows Defender / AV status | `Get-MpComputerStatus` |
| 2 | Quick malware scan + active threats | `Start-MpScan` + `Get-MpThreat` |
| 3 | System file integrity | `sfc /verifyonly` |
| 4 | Windows image health | `dism /CheckHealth` (admin only) |
| 5 | Disk SMART status | `Get-PhysicalDisk` |
| 6 | Startup persistence | `Win32_StartupCommand` + keyword detection |

  Split-pane UI: SCAN LOG (human-readable) + RAW TERMINAL OUTPUT (exact commands + `[ADMIN]`/`[no admin]` tag). Spinner + elapsed time + stall warning.

- **🧬 Full Deep Scan** — extended health scan covering all 6 steps plus additional heuristic checks; longer runtime with more detailed output
- **System Fixer** — Full Repair (threat removal → SFC → DISM), SFC Only, DISM Only

### 🔐 CRYPT — Cryptography

- **ENCRYPT** — AES-256-GCM, RSA encryption for files or text input
- **DECRYPT** — decrypt output from any supported algorithm
- **INSPECT** — detect encryption type, analyze ciphertext structure, identify algorithm markers
- **HASH** — compute MD5, SHA-1, SHA-256, SHA-512, SHA-3, BLAKE2 for files or strings; compare hashes
- **VIGENÈRE** — polyalphabetic cipher encoder/decoder with key analysis

### 👁 WD — Watchdog

Folder monitor with real-time change alerts. Configurable watch paths, event types (create, modify, delete, rename), alert actions (log, notification, auto-quarantine). Runs as a background thread; toggle per-session or set to start automatically.

### ⚠ DZ — Danger Zone

Advanced operations for power users and debugging:

- Scan data management (purge, export, import)
- Database tools (vacuum, integrity check, manual query)
- Configuration reset and backup
- YARA rule bulk operations
- Quarantine management
- Sandbox and watcher controls
- Network and API diagnostics
- Backup and restore tools
- Crash simulation (all crash codes including trampoline, recovery, sentinel, version missing)
- System operations (uninstall / reinstall triggers)
- System diagnostics and debug log viewer
- Performance and optimization tools
- Secure wipe
- Nuclear options (full reset)

---

## Supported APIs

All services are optional. No key is required to use local analysis features.

| Service | Used for |
|---------|---------|
| VirusTotal | File scan, hash lookup, bulk batch, URL scan, rescan |
| MalwareBazaar | Hash lookup, sample download |
| AbuseIPDB | IP reputation scoring |
| URLScan.io | URL analysis and screenshot |
| AlienVault OTX | IOC reputation, pulse lookup |
| Shodan | Host info, open ports, banners |
| GreyNoise | IP noise classification |
| HybridAnalysis | Sandbox submission and result retrieval |

---

## Folder Structure

```
V0rtex_System/
├── V0RTEX_v1.0.0.X0/               ← main install directory
│   ├── v0rtex.py                   ← the entire application (single file)
│   ├── config.json                 ← all user settings and API keys
│   ├── scan_history.db             ← SQLite scan database
│   ├── whitelist.txt               ← SHA-256 hash exclusions
│   ├── notes.txt                   ← persistent scratchpad
│   ├── rules_state.json            ← YARA library download state
│   ├── todo_list.json              ← TODO tab data
│   ├── snippets.json               ← Snippets library data
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
│   │   ├── recovery_ops/           ← persistent Recovery UI logs
│   │   ├── crash_log/
│   │   ├── session_log/
│   │   ├── update_log/
│   │   ├── setup_log/
│   │   ├── trampoline_log/
│   │   └── admin_log/
│   ├── quarantine/                 ← isolated files
│   ├── backups/                    ← auto-created backup ZIPs
│   ├── _recovery/                  ← recovery system working directory
│   ├── sandbox_env/
│   │   └── drop/                   ← auto-scan drop folder
│   ├── threat_feeds/               ← imported threat feed files
│   └── pcap_dumps/                 ← packet capture output
├── v0rtex_utils/
│   ├── .vx_meta/
│   │   └── vx_version              ← version JSON (read by app and Recovery UI)
│   ├── debug_log/
│   │   └── Crash_Full_Report/
│   ├── v0rtex_updater.py           ← standalone updater
│   ├── v0rtex_recovery_ui.py       ← standalone recovery UI
│   ├── v0rtex_reinstall.py         ← reinstall wizard (auto-generated on first setup)
│   └── v0rtex_uninstall.py         ← uninstall wizard (auto-generated on first setup)
└── V0rtex_backups/                 ← backup ZIPs (outside V0rtex_System)
```

---

## Security Notes

V0RTEX requires administrator rights for some features (System Check/Fixer, Defender interaction, process monitoring, network capture). It will run with limited rights, but some tabs will be restricted.

Sensitive PowerShell and system commands are assembled at runtime from string fragments rather than stored as literals in the source. This reduces AV false positives from static string pattern matching. The version string itself is never stored as a literal — it is read from `.vx_meta/vx_version` or assembled at runtime.

If Windows Defender flags V0RTEX, add the install folder to your Defender exclusion list. The setup wizard does this automatically.

Do not use V0RTEX as your sole security solution. It is a lab tool and its scan results should be treated as informational, not definitive.

---

## Crash Recovery

If V0RTEX crashes on startup or mid-session, a **Recovery Terminal** launches automatically. From there you can:

- View the crash report and session log
- Clean TEMP files
- Reinstall dependencies
- Roll back to a previous backup (version picker with timestamps)
- Perform a full reinstall

Crash reports are saved to `debug_log/crash_log/` with timestamps. Recovery operations are logged persistently to `debug_log/recovery_ops/`.

The standalone `v0rtex_recovery_ui.py` in `v0rtex_utils/` can be launched independently if the main app fails to start entirely.

---

## Updating

V0RTEX has a built-in updater (CFG → UPDATER) and a standalone updater script (`v0rtex_utils/v0rtex_updater.py`).

Update flow:
1. Check remote `version.txt` for new version
2. Download new `v0rtex.py` from the release branch
3. Create a timestamped backup ZIP of current install (config, rules, reports, DB preserved)
4. Launch `v0rtex_adapter.py` which handles: kill processes → remove obsolete deps → install/upgrade deps → rebuild dirs → write version metadata → launch new version
5. If the external launcher outside `V0rtex_System/` is detected, it is patched automatically

Auto-update check can be toggled in CFG → CONFIGURATION.

---

## Version Scheme

```
MAJOR . BIG_UPDATE . SMALL_UPDATE . X[BUGFIX]

Example: 1.0.0.X0
  1       = major version
  0       = big update (significant feature batch)
  0       = small update (incremental features or fixes)
  X0      = first release on top of 1.0.0
  X1      = bugfix release
```

---

## License

Copyright © 2024–2026 Vider_06. All rights reserved.  
See [LICENSE.txt](LICENSE.txt) for full terms.
