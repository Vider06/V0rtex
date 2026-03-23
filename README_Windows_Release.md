# V0RTEX v1.0.1.X0

**V0RTEX** is a self-contained Windows malware analysis platform built entirely in Python + Tkinter.  
One file. No external launcher. No installer required beyond running `python v0rtex.py`.

> `V = Vulnerability · O = Oriented · R = Recon · T = Threat · E = Exploitation · X = eXaminer`

**Author:** Vider_06  
**Platform:** Windows 10 / 11 (64-bit) only  
**Python:** 3.10 or higher — including 3.12, 3.13, 3.14  
**License:** Copyright © 2024–2026 Vider_06 — All rights reserved. See [LICENSE](https://github.com/Vider06/V0rtex/blob/main/LICENSE).

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
  - [🔐 CRYPT — Cryptography](#-crypt--cryptography)
- [Supported APIs](#supported-apis)
- [Security Notes](#security-notes)
- [Crash Recovery](#crash-recovery)
- [Updating](#updating)
- [Version Scheme](#version-scheme)
- [Contributing](#contributing)
- [License](#license)

---

## What is V0RTEX?

V0RTEX is a complete malware analysis lab that lives inside a single Python script (~35,000 lines). It covers the full analysis workflow: from initial triage and static analysis (hashes, PE headers, strings, entropy, YARA) through dynamic monitoring (process tree, network connections, PCAP capture, sandbox) to post-analysis reporting (HTML/JSON/PDF exports, SQLite history, MITRE ATT&CK mapping). It also includes network privacy tools (Proxy, Tor, Noise Generator), a self-protection layer, a trampoline-based auto-updater, a full Windows system health checker, and a standalone Recovery UI — all built directly into the UI with no external tools required beyond Python.

---

## Features at a Glance

| Area | Details |
|---|---|
| **YARA** | Custom rule editor · Community library downloader · String deobfuscator · Sigma rule viewer · yara-python / yara-x multi-engine |
| **VirusTotal** | File scan · Hash lookup · Bulk batch · Auto-upload · Rescan scheduling |
| **PE Inspector** | Headers · Imports · Exports · Sections · Suspicious API detection · Per-section entropy · Import Hash (imphash) |
| **IOC** | Auto-extraction (IPs, domains, URLs, hashes, emails, CVEs, registry keys, Win APIs) · MITRE ATT&CK mapping · Feed import · IP/Domain reputation · Secrets scanner |
| **Sandbox** | Auto-scan watched folder · Process monitor · File analyzer · String extraction · Cuckoo/CAPE integration |
| **Network** | Live connections · PCAP (tshark) · Port scan · DNS · WHOIS · SSL/TLS · HTTP headers · URL tools · Ping · **Proxy** · **Tor** · **Noise generator** · **Live traffic monitor** · **Connection stats** |
| **Crypto / Encoding** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Vigenère · Base64/Hex/XOR · JWT decoder · Hash inspector · ROT |
| **Threat APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan · AlienVault OTX · Shodan · GreyNoise · HybridAnalysis |
| **Entropy** | File entropy chart · Section-level analysis · Verdict gauge |
| **Process** | Live scanner · Service viewer · Startup items · Env variables · Open handles · Process tree · Registry browser |
| **Lookup** | Hash · HEX · REGEX · DOC · SIG · BATCH · DIFF · ARCHIV · MACRO · B64 · XOR · BCONV · JWT · ROT · PE-HDR · UNICODE · BINPAT · **Fuzzy hash** |
| **Notes** | Scratchpad · MITRE map · TODO list · Snippet library |
| **Defense** | Real-time watchdog · Quarantine · Self-defense · App integrity · Folder protection · Auto-backup · Emergency rollback |
| **Privacy** | Log censor · Auto-censor toggle · Temp log storage management |
| **Performance** | Throttle toggle · Max workers · Chunk size · Scan delay · Niceness slider |
| **System Check** | Defender status · Quick malware scan · SFC · DISM · Disk SMART · Startup persistence · System Fixer · Full deep scan |
| **DB** | SQLite · Full scan history · Export CSV/JSON/HTML · Scan history browser |
| **Updater** | Auto-update check · Adapter-based pipeline · Trampoline chain for large version gaps · Self-updating adapter · Dep cleanup · Fresh install / data reset modes |
| **Recovery** | Standalone Recovery UI · Version tab with rollback · Animated repair operations · Persistent recovery logs |

**21 main tabs · 90+ sub-tabs**

---

## Requirements

- Windows 10 or 11 (64-bit)
- Python 3.10 or higher → [python.org](https://www.python.org/downloads/)
- Internet connection (for setup, API lookups, YARA library download, updates)
- Administrator rights — recommended for full functionality (process monitoring, network capture, SFC/DISM)

---

## Installation

### 1. Clone or download

```
git clone -b Windows_Release https://github.com/Vider06/V0rtex.git
cd V0rtex
```

Or download `v0rtex.py` directly from the [Releases](https://github.com/Vider06/V0rtex/releases) page.

### 2. Run

```
python v0rtex.py
```

> On first launch, V0RTEX detects that it hasn't been set up yet and opens the **Setup Wizard** automatically.

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
├── V0RTEX_v1.0.1.X0/               ← main install directory
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
│   ├── quarantine/                 ← isolated files
│   ├── backups/                    ← auto-created backup ZIPs
│   ├── _recovery/                  ← recovery system working directory
│   ├── sandbox_env/
│   │   └── drop/                   ← auto-scan drop folder
│   ├── threat_feeds/               ← imported threat feed files
│   └── pcap_dumps/                 ← packet capture output
├── v0rtex_utils/
│   ├── .vx_meta/
│   │   └── vx_version              ← JSON version metadata
│   ├── v0rtex_updater.py           ← standalone updater
│   ├── v0rtex_recovery_ui.py       ← standalone recovery UI
│   ├── v0rtex_adapter.py           ← post-update adapter (self-updating)
│   ├── censor_config.json          ← log censor rule selection
│   ├── Temp_Log_Storage/           ← uncensored log buffer
│   ├── UNCENSORED/                 ← preserved original logs
│   ├── debug_log/
│   │   ├── crash_log/
│   │   ├── session_log/
│   │   ├── update_log/
│   │   ├── trampoline_log/
│   │   ├── admin_log/
│   │   ├── setup_log/
│   │   └── recovery_ops/           ← persistent Recovery UI logs
│   └── Crash_Full_Report/
└── V0rtex_backups/                 ← backup ZIPs (outside V0rtex_System)
```

---

## Tab Reference

### 🏠 HOME

Three sub-tabs:

- **📊 DASHBOARD** — live scan counters (total, malicious, clean, YARA hits, queue, active APIs), threat level bar, recent scans table. Quick Actions: Add File, Add Folder, Scan URL, Sandbox, AutoScan, Watch Folder. Clicking any row opens the full scan report popup.
- **ℹ INFO** — system information, installed dependencies status, runtime diagnostics.
- **README** — embedded README viewer.

### 📋 LOGS

Two live log panels: **FILE OPERATIONS** (every scan with verdict and timing) and **DEBUG LOG** (internal checkpoints, background thread activity, errors). Logs are mirrored to `debug_log/` on disk. Clear and export to `.txt`.

### 📊 CHRT — Charts

- **Charts** — live bar/pie charts of scan results.
- **ENT** — entropy distribution histogram across all scanned files.
- **HEAT** — heatmap of threat categories vs file types.

### 📁 REP — Reports

Browse, open and delete scan reports. HTML, JSON and plain text. Side-by-side diff view for comparing two reports.

### 🎯 IOC

- **IOC** — auto-extracts IPs, domains, URLs, hashes, emails, CVEs, registry keys, Windows API names.
- **EXTRACT** — targeted extraction with regex filtering.
- **MITRE** — maps IOCs to MITRE ATT&CK techniques.
- **Feed** — import external threat feed files (CSV, JSON, TXT).
- **Reputation** — bulk IP/domain reputation via configured APIs.
- **Secrets** — detects API keys, tokens, credentials embedded in files.
- **IMPHASH** — PE Import Hash Analyzer for malware family clustering via `pefile`. Single file and bulk folder scan.
- **STATS** — IOC statistics dashboard.
- **IOCEXP** — IOC export in multiple formats.

### 🛡 YARA

- **YARA** — run rules against any file, view hits with rule name, namespace and matched strings.
- **LIBRARY** — download community rule sets from GitHub. Tracks download state per repo.
- **RULE EDITOR** — full YARA authoring with syntax highlighting, compile & test, test-on-file.
- **DEOBF** — deobfuscation: XOR brute-force, Base64, ROT, hex decode.
- **SIGMA** — load and view Sigma `.yml` detection rules.

### ⚡ PERF

System performance monitor: CPU%, RAM, disk I/O, network I/O, per-process breakdown. Refreshes every 5 seconds.

### ⏱ TL — Timeline

Chronological scan history chart plotted by verdict, file type and entropy over time.

### 🔬 SB — Sandbox

- **Auto-Scan** — folder watcher: drop a file in `sandbox_env/drop/` and it gets scanned automatically.
- **Process** — live process list with right-click scan/kill/inspect.
- **File Analyzer** — deep static analysis: magic bytes, entropy, PE info, strings, IOC extraction, YARA.
- **Cuckoo/CAPE** — submit to and retrieve results from a local Cuckoo or CAPE instance.

### 🏗 SETUP

The setup and reinstall wizard, accessible without restarting. Reinstall dependencies, reconfigure paths, or fully reinstall V0RTEX in place.

### ⚙ CFG — Configuration

- **API KEYS** — manage API keys for all supported services.
- **CONFIGURATION** — tshark path, proxy settings, request delay, auto-update toggle.
- **WHITELIST** — SHA-256 hash exclusions.
- **EXPORT** — export config, scan history and notes.
- **CHECKPOINT** — save and restore named snapshots of the full app state.
- **SCAN HISTORY** — full SQLite browser with filter, search and export.
- **DEBUG LOGS** — browse and open debug log files.
- **UPDATE LOG** — full update history from `debug_log/update_log/`.
- **UPDATER** — check for updates, configure auto-check, view update history.

### 🔎 LOOK — Lookup

Hash · HEX viewer · REGEX tester · DOC inspector · SIG (signature) viewer · BATCH scanner · DIFF (side-by-side file diff) · ARCHIV (archive inspector) · MACRO (Office macro extractor) · B64 (Base64 encode/decode) · XOR (XOR brute-force) · BCONV (binary/hex converter) · JWT decoder · ROT cipher · PE-HDR (PE header dump) · UNICODE (string normalizer) · BINPAT (binary pattern search) · **FUZZY** (fuzzy hash similarity via rolling hash + Jaccard scoring)

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
- **Ping** — ICMP ping utility.
- **🔀 Proxy** — HTTP/HTTPS/SOCKS5 proxy manager. ARM / STOP / Test. Applied to all V0RTEX network requests.
- **🧅 Tor** — anonymous routing via Tor. Auto-detects binary, winget install fallback. Start / Stop / New Identity / Check IP. Routes all requests through SOCKS5 127.0.0.1:9050 when armed.
- **📡 Noise Gen** — network noise generator to mask real traffic patterns. ARM / STOP with live stats.
- **📡 Live Traffic** — real-time per-interface traffic monitor with rolling bytes/s graph.
- **📊 Conn Stats** — live connection state graph: ESTABLISHED / TIME_WAIT / CLOSE_WAIT / other over time.

### 📝 NOTES

- **Notepad** — persistent scratchpad saved to `notes.txt`.
- **MITRE ATT&CK** — searchable technique reference.
- **TODO** — task list with checkboxes, saved to `todo_list.json`.
- **Snippets** — code/IOC snippet library saved to `snippets.json`.

### ⚙ SET — Global Settings

Sub-tabs: Interface · Scan · **Privacy** · Paths · Network · Defense · Notifications · **⚡ Performance** · Advanced · Automatic Actions

**PRIVACY** sub-tab:
- Auto-censor logs toggle — redacts API keys, file paths, IPs, hashes, credentials from all log output
- Per-category censor rule selection (saved to `censor_config.json`)
- Flush `Temp_Log_Storage` with UNCENSORED preservation
- Open V0RTEX LOG CENSOR standalone window

**⚡ PERFORMANCE** sub-tab:
- Throttle scan threads toggle
- Max background workers spinner
- Chunk size slider for large file processing
- Scan thread delay (ms)
- Niceness slider (background thread priority)
- Cross-link to Advanced tab

### 🔒 PROT — App Protection

- **Build/Destroy** — set up and tear down the protected environment.
- **Protected Folders** — monitor folders for unauthorized changes.
- **Integrity** — hash-based verification of all V0RTEX files.
- **Defense** — real-time defense engine with auto-quarantine.
- **Self-Defense** — process-level protection against termination.
- **Backup** — create and restore full lab ZIP backups. Emergency rollback button restores from the most recent backup without going through the updater.
- **System Check** — 6-step Windows health scan (see below).
- **Watchdog** — file system watcher with configurable alerts.

#### System Check (PROT → System Check)

| Step | Check | Tool used |
|---|---|---|
| 1 | Windows Defender / AV status | `Get-MpComputerStatus` |
| 2 | Quick malware scan + active threat list | `Start-MpScan` + `Get-MpThreat` |
| 3 | System file integrity | `sfc /verifyonly` (direct, not via PowerShell pipe) |
| 4 | Windows image health | `dism /CheckHealth` (admin only) |
| 5 | Disk SMART status | `Get-PhysicalDisk` |
| 6 | Startup persistence | `Win32_StartupCommand` + suspicious keyword detection |

Split-pane UI: **SCAN LOG** left (human-readable results), **RAW TERMINAL OUTPUT** right (exact command + `[ADMIN]`/`[no admin]` tag). Spinner + elapsed time + stall warning. Auto-prompts **System Fixer** on issues.

A **🧬 FULL SCAN** sub-tab provides an extended deep-inspection pass beyond the 6 standard steps.

#### System Fixer

- **Full Repair** — threat removal → SFC (`sfc /scannow`) → DISM (`dism /RestoreHealth`) in sequence.
- **SFC Only** — run SFC independently.
- **DISM Only** — run DISM independently.

Progress bar uses `indeterminate` mode during long operations.

### 🔐 CRYPT — Cryptography

- **ENCRYPT** — AES-256-GCM, RSA, Vigenère.
- **DECRYPT** — counterpart to all encrypt modes.
- **INSPECT** — hash inspector: SHA-3, BLAKE2, MD5, SHA-1, SHA-256 side by side.

---

## Supported APIs

All integrations are optional — no key is required to use local analysis features.

| Service | Used for |
|---|---|
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

V0RTEX requires administrator rights for some features (System Check/Fixer, Defender interaction, process monitoring). It will work with limited rights but some tabs will be restricted.

Sensitive PowerShell/system commands and the version string are never stored as literals in the source — they are assembled at runtime from fragments or read from `.vx_meta/vx_version`. This reduces false positives from antivirus engines.

If Windows Defender flags V0RTEX, add the install folder to your Defender exclusion list. The setup wizard does this automatically.

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

When an update is triggered:

1. V0RTEX creates an `EMERGENCY_RESTORE.zip` backup of the current install and a userdata backup.
2. Downloads `v0rtex_adapter.py` from GitHub and spawns it with a `meta.json` containing all parameters.
3. V0RTEX exits so the adapter can freely overwrite files.
4. The adapter **self-updates first** — fetches its own latest version from GitHub and relaunches if newer.
5. If the version gap is large, the adapter runs a **trampoline loop**: fetches `compat_map.json` from GitHub, installs each intermediate version silently in sequence until one hop before the target.
6. The final install runs through the full 6-step pipeline: Kill → Deps cleanup → Pip install → Rebuild dirs → Write metadata → Launch.
7. If launch fails, the adapter restores from the emergency backup automatically.

Auto-update check can be toggled in CFG → CONFIGURATION.

---

## Version Scheme

```
MAJOR . BIG_UPDATE . SMALL_UPDATE . X[BUGFIX]

Example: 1.0.1.X0
  1       = major version
  0       = big update batch
  1       = small update
  X0      = first release on this version
```

---

## Contributing

Issues and pull requests are welcome. If you find a bug, open an issue with:

- V0RTEX version (shown in the bottom status bar)
- Python version (`python --version`)
- Windows version
- The contents of the relevant crash report from `debug_log/crash_log/`

---

## License

Copyright © 2024–2026 Vider_06. All rights reserved.  
See [LICENSE](https://github.com/Vider06/V0rtex/blob/main/LICENSE) for full terms.
