# V0RTEX v1.0.1.X1

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
  - [⚠ DZ — Danger Zone](#-dz--danger-zone)
- [Supported APIs](#supported-apis)
- [Security Notes](#security-notes)
- [Crash Recovery](#crash-recovery)
- [Updating](#updating)
- [Version Scheme](#version-scheme)
- [Contributing](#contributing)
- [License](#license)

---

## What is V0RTEX?

V0RTEX is a complete malware analysis lab inside a single Python script (~35,000 lines). It covers the full analysis workflow: from initial triage and static analysis (hashes, PE headers, strings, entropy, YARA) through dynamic monitoring (process tree, network connections, PCAP capture, sandbox) to post-analysis reporting (HTML/JSON/PDF exports, SQLite history, MITRE ATT&CK mapping). It also includes network privacy tools (Proxy, Tor, Noise Generator), a self-protection layer, a trampoline-based auto-updater, a full Windows system health checker, and a standalone Recovery UI — all in a single file with no external tools required beyond Python.

---

## Features at a Glance

| Area | Details |
|---|---|
| **YARA** | Custom rule editor · Community library downloader · String deobfuscator · Sigma rule viewer · yara-python / yara-x multi-engine |
| **VirusTotal** | File scan · Hash lookup · Bulk batch · Auto-upload · Rescan scheduling |
| **PE Inspector** | Headers · Imports · Exports · Sections · Suspicious API detection · Per-section entropy · Import Hash (imphash) |
| **IOC** | Auto-extraction (IPs, domains, URLs, hashes, emails, CVEs, registry keys, Win APIs) · MITRE ATT&CK mapping · Feed import · IP/Domain reputation · Secrets scanner |
| **Sandbox** | Auto-scan drop folder · Process monitor · File analyzer · String extraction · Cuckoo/CAPE integration |
| **Network** | Live connections · PCAP (tshark) · Port scan · DNS · WHOIS · SSL/TLS · HTTP headers · URL tools · Ping · Proxy · Tor · Noise generator · Live traffic monitor · Connection stats |
| **Crypto / Encoding** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Vigenère · Base64/Hex/XOR · JWT decoder · Hash inspector · ROT |
| **Threat APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan · AlienVault OTX · Shodan · GreyNoise · HybridAnalysis |
| **Entropy** | File entropy chart · Section-level analysis · Verdict gauge |
| **Process** | Live scanner · Service viewer · Startup items · Env variables · Open handles · Process tree · Registry browser |
| **Lookup** | Hash · HEX · REGEX · DOC · SIG · BATCH · DIFF · ARCHIV · MACRO · B64 · XOR · BCONV · JWT · ROT · PE-HDR · UNICODE · BINPAT · Fuzzy hash |
| **Notes** | Scratchpad · MITRE map · TODO list · Snippet library |
| **Defense** | Real-time watchdog · Quarantine · Self-defense · App integrity · Folder protection · Auto-backup · Emergency rollback |
| **Privacy** | Log censor · Auto-censor toggle · Per-category rules · Temp log storage management |
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

> On first launch V0RTEX detects it hasn't been set up yet and opens the **Setup Wizard** automatically.

### 3. Setup Wizard

The setup wizard handles everything automatically:

- Installs all Python dependencies via `pip` (bulk install + per-package fallback + trusted hosts)
- Installs YARA using the multi-engine chain:
  1. `yara-python-wheel` — precompiled wheel, no compiler needed
  2. `yara-x` — Rust-based, no compiler needed, full API shim
  3. VS Build Tools + `yara-python` from source — last resort, shown only after user confirmation
- Auto-detects and optionally installs Wireshark/tshark (checks registry, known paths, `shutil.which`)
- Creates the full folder structure under `V0rtex_System/`
- Writes `config.json`, `whitelist.txt`, `notes.txt` with factory defaults
- Creates `scan_history.db` (SQLite)
- Generates all utility scripts in `v0rtex_utils/`
- Adds Windows Defender exclusions for the install folder

### 4. Configure API keys

Go to **CFG** → **API KEYS** and enter your keys for VirusTotal, MalwareBazaar, AbuseIPDB, URLScan, AlienVault OTX, Shodan, GreyNoise, HybridAnalysis.

Keys are stored locally in `config.json`. None are required — they only unlock cloud lookup features.

### 5. Download YARA rules (optional but recommended)

Go to **YARA** → **LIBRARY** → select repositories (Neo23x0, Elastic, Avast, JPCERT/CC, VirusTotal, Yara-Rules, mikesxrs) → click **DOWNLOAD**.

---

## Folder Structure

Items marked `[setup]` are created by the Setup Wizard on first run. Items marked `[startup]` are created automatically every time V0RTEX launches.

```
V0rtex_System/
├── V0RTEX_v1.0.1.X1/               ← main install directory
│   ├── v0rtex.py                   [setup]   the entire application
│   ├── config.json                 [setup]   all settings and API keys
│   ├── config.json.bak             [runtime] auto-backup before config changes
│   ├── scan_history.db             [setup]   SQLite scan database
│   ├── whitelist.txt               [setup]   SHA-256 hash exclusions
│   ├── notes.txt                   [setup]   persistent scratchpad
│   ├── requirements.txt            [setup]   pip dependencies
│   ├── launch.bat                  [setup]   quick launch script
│   ├── _setup_complete             [setup]   sentinel — marks completed install
│   ├── modules/                    [setup]
│   │   ├── __init__.py
│   │   ├── pe_analysis.py
│   │   ├── cuckoo_api.py
│   │   ├── secret_scanner.py
│   │   └── wireshark.py
│   ├── rules/                      [startup]
│   │   ├── rules_state.json        [setup]
│   │   └── external/               ← community YARA rule sets
│   ├── reports/                    [startup]  HTML/JSON scan reports
│   ├── reports_pdf/                [setup]    PDF reports
│   ├── quarantine/                 [startup]  isolated files (.quar, XOR-obfuscated)
│   ├── backups/                    [startup]  auto-created backup ZIPs
│   ├── _recovery/                  [startup]  recovery working directory
│   ├── sandbox_env/                [setup]
│   │   └── drop/                   ← auto-scan drop folder
│   ├── threat_feeds/               [setup]    imported threat feed files
│   ├── pcap_dumps/                 [setup]    tshark packet captures
│   ├── app_usage_log/              [startup]  per-feature activity logs
│   │   ├── conn_quality/
│   │   ├── live_traffic/
│   │   ├── noise_gen/
│   │   ├── proxy/
│   │   ├── tor/
│   │   └── UNCENSORED/
│   └── Quality_Capture/            [startup]  quality/diagnostic captures
│
├── v0rtex_utils/                   ← utility scripts and all system logs
│   ├── .vx_meta/
│   │   └── vx_version              [setup/adapter]  JSON version metadata
│   ├── _v0rtex_running.lock        [runtime]  single-instance lock file
│   ├── censor_config.json          [runtime]  log censor rule selection
│   ├── v0rtex_updater.py           [setup]
│   ├── v0rtex_recovery_ui.py       [setup]
│   ├── v0rtex_reinstall.py         [setup]
│   ├── v0rtex_uninstall.py         [setup]
│   ├── v0rtex_log_censor.py        [setup]
│   ├── Crash_Full_Report/          [setup]
│   ├── Temp_Log_Storage/           [startup]  buffered logs pending censor flush
│   │   ├── session_log/
│   │   ├── silent_log/
│   │   ├── conn_quality/
│   │   ├── live_traffic/
│   │   ├── noise_gen/
│   │   ├── proxy/
│   │   ├── tor/
│   │   ├── admin_log/
│   │   ├── setup_log/
│   │   ├── recovery_ops/
│   │   └── update_log/
│   ├── UNCENSORED/                 [startup]  original copies before censoring
│   │   └── (same subdirs as Temp_Log_Storage)
│   └── debug_log/                  [startup]  all persistent logs
│       ├── admin_status.log        [runtime]
│       ├── admin_log/
│       ├── crash_log/
│       ├── session_log/
│       ├── trampoline_log/
│       ├── update_log/
│       └── UNCENSORED/
│           └── (same subdirs)
│
└── V0rtex_backups/                 ← outside V0rtex_System — backup ZIPs
```

---

## Tab Reference

### 🏠 HOME

- **📊 DASHBOARD** — live scan counters (total, malicious, clean, YARA hits, queue, active APIs), threat level bar, recent scans table with click-to-open report. Quick Actions: Add File, Add Folder, Scan URL, Sandbox, AutoScan, Watch Folder.
- **ℹ INFO** — system info, installed dependency status, runtime diagnostics.
- **README** — embedded README viewer.

### 📋 LOGS

Two live panels: **FILE OPERATIONS** (every scan with verdict and timing) and **DEBUG LOG** (internal checkpoints, errors). Mirrored to `v0rtex_utils/debug_log/`. Clear and export to `.txt`.

### 📊 CHRT — Charts

**Charts** · **ENT** (entropy histogram) · **HEAT** (threat category heatmap)

### 📁 REP — Reports

Browse, open and delete HTML/JSON/text scan reports. Side-by-side diff view.

### 🎯 IOC

- **IOC** — auto-extracts IPs, domains, URLs, hashes, emails, CVEs, registry keys, Win APIs.
- **EXTRACT** — targeted extraction with regex filtering.
- **MITRE** — maps IOCs to MITRE ATT&CK techniques.
- **Feed** — import threat feed files (CSV, JSON, TXT).
- **Reputation** — bulk IP/domain reputation via configured APIs.
- **Secrets** — detects API keys, tokens, credentials embedded in files.
- **IMPHASH** — PE Import Hash Analyzer for malware family clustering. Single file and bulk folder scan.
- **STATS** — IOC statistics dashboard.
- **IOCEXP** — IOC export in multiple formats.

### 🛡 YARA

- **YARA** — run rules against any file, view hits with rule name, namespace, matched strings.
- **LIBRARY** — download community rule sets from GitHub.
- **RULE EDITOR** — full YARA authoring with syntax highlighting, compile & test.
- **DEOBF** — XOR brute-force, Base64, ROT, hex decode.
- **SIGMA** — load and view Sigma `.yml` detection rules.

### ⚡ PERF

System performance monitor: CPU%, RAM, disk I/O, network I/O, per-process breakdown.

### ⏱ TL — Timeline

Chronological scan history chart by verdict, file type and entropy over time.

### 🔬 SB — Sandbox

- **Auto-Scan** — drop folder watcher: files in `sandbox_env/drop/` are scanned automatically.
- **Process** — live process list with right-click scan/kill/inspect.
- **File Analyzer** — deep static: magic bytes, entropy, PE info, strings, IOC, YARA.
- **Cuckoo/CAPE** — submit to and retrieve results from a local Cuckoo or CAPE instance.

### 🏗 SETUP

Setup and reinstall wizard accessible without restarting.

### ⚙ CFG — Configuration

**API KEYS** · **CONFIGURATION** · **WHITELIST** · **EXPORT** · **CHECKPOINT** · **SCAN HISTORY** · **DEBUG LOGS** · **UPDATE LOG** · **UPDATER**

### 🔎 LOOK — Lookup

Hash · HEX · REGEX · DOC · SIG · BATCH · DIFF · ARCHIV · MACRO · B64 · XOR · BCONV · JWT · ROT · PE-HDR · UNICODE · BINPAT · **FUZZY** (fuzzy hash via rolling hash + Jaccard scoring)

### 🖥 PROC — Processes

**Processes** · **Services** · **Startup Items** · **Env Variables** · **Handles** · **Proc Tree** · **Registry**

### 🌐 NET — Network

- **Connections** — live TCP/UDP with remote IP, port, process.
- **URL Tools** — encode/decode, expand shortened URLs.
- **IP/Domain Rep.** — bulk reputation lookup.
- **DNS** — A, AAAA, MX, TXT, NS, CNAME lookups.
- **WHOIS** — full WHOIS data.
- **HTTP Headers** — raw header inspector.
- **SSL/TLS** — certificate chain viewer.
- **Port Scan** — TCP scanner with configurable range.
- **PCAP** — start/stop tshark capture, open in Wireshark.
- **Ping** — ICMP ping utility.
- **🔀 Proxy** — HTTP/HTTPS/SOCKS5 proxy manager. ARM / STOP / Test. Applied to all V0RTEX network requests.
- **🧅 Tor** — anonymous routing. Auto-detects binary, winget install fallback. Start / Stop / New Identity / Check IP. Routes through SOCKS5 127.0.0.1:9050 when armed.
- **📡 Noise Gen** — background traffic generator to mask real activity. ARM / STOP with live stats.
- **📡 Live Traffic** — real-time per-interface bytes/s with rolling graph.
- **📊 Conn Stats** — live connection state graph: ESTABLISHED / TIME_WAIT / CLOSE_WAIT / other.

### 📝 NOTES

**Notepad** · **MITRE ATT&CK** · **TODO** · **Snippets**

### ⚙ SET — Global Settings

**Interface** · **Scan** · **Privacy** · **Paths** · **Network** · **Defense** · **Notifications** · **⚡ Performance** · **Advanced** · **Automatic Actions**

**PRIVACY** — auto-censor logs, per-category rule selection (API keys, IPs, paths, hashes, credentials, Tor, proxy, noise), `Temp_Log_Storage` flush, open LOG CENSOR window.

**⚡ PERFORMANCE** — throttle scans, max background workers, chunk size, thread delay (ms), niceness slider, cross-link to Advanced.

### 🔒 PROT — App Protection

- **Build/Destroy** — set up and tear down the protected environment.
- **Protected Folders** — monitor folders for unauthorized changes.
- **Integrity** — hash-based verification of all V0RTEX files.
- **Defense** — real-time defense engine with auto-quarantine.
- **Self-Defense** — process-level protection against termination.
- **Backup** — create and restore full lab ZIP backups. Emergency rollback restores from the most recent backup without going through the updater.
- **System Check** — 6-step Windows health scan.
- **Watchdog** — file system watcher with configurable alerts.

#### System Check (PROT → System Check)

| Step | Check | Tool |
|---|---|---|
| 1 | Windows Defender / AV status | `Get-MpComputerStatus` |
| 2 | Quick malware scan + active threats | `Start-MpScan` + `Get-MpThreat` |
| 3 | System file integrity | `sfc /verifyonly` (direct call) |
| 4 | Windows image health | `dism /CheckHealth` (admin only) |
| 5 | Disk SMART status | `Get-PhysicalDisk` |
| 6 | Startup persistence | `Win32_StartupCommand` + keyword detection |

Split-pane: SCAN LOG left, RAW TERMINAL OUTPUT right with `[ADMIN]`/`[no admin]` tags. Spinner + elapsed time + stall warning. Auto-prompts System Fixer on issues. **🧬 FULL SCAN** sub-tab for extended deep-inspection.

#### System Fixer

**Full Repair** (threat removal → SFC → DISM) · **SFC Only** · **DISM Only** — `indeterminate` progress bar during long operations.

### 🔐 CRYPT — Cryptography

**ENCRYPT** (AES-256-GCM, RSA, Vigenère) · **DECRYPT** · **INSPECT** (SHA-3, BLAKE2, MD5, SHA-1, SHA-256)

### ⚠ DZ — Danger Zone

Crash simulator, error code reference (105 entries), admin permission management, diagnostic tools.

---

## Supported APIs

All integrations are optional — no key required for local analysis.

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

V0RTEX requires administrator rights for some features (System Check/Fixer, Defender interaction, process monitoring). Works with limited rights but some tabs will be restricted.

Sensitive PowerShell/system commands and the version string are never stored as literals in source — assembled at runtime from fragments or read from `.vx_meta/vx_version`. This reduces AV false positives.

If Windows Defender flags V0RTEX, add the install folder to your Defender exclusion list. The setup wizard does this automatically.

---

## Crash Recovery

If V0RTEX crashes, a **Recovery Terminal** launches automatically. From there you can view the crash report, clean TEMP files, reinstall dependencies, roll back to a previous backup, or perform a full reinstall.

Crash reports are saved to `v0rtex_utils/debug_log/crash_log/`. Recovery logs persist in `v0rtex_utils/debug_log/` (also buffered in `Temp_Log_Storage/`).

The standalone `v0rtex_recovery_ui.py` in `v0rtex_utils/` can be launched independently if the main app fails to start entirely.

---

## Updating

V0RTEX has a built-in updater (CFG → UPDATER) and a standalone updater (`v0rtex_utils/v0rtex_updater.py`).

When an update is triggered:

1. V0RTEX creates an `EMERGENCY_RESTORE.zip` backup and a userdata backup.
2. Downloads `v0rtex_adapter.py` from GitHub and spawns it with a `meta.json`.
3. V0RTEX exits so the adapter can freely overwrite files.
4. The adapter **self-updates first** — fetches its own latest version and relaunches if newer.
5. If the version gap is large, the adapter runs a **trampoline loop**: fetches `compat_map.json`, installs each intermediate version silently until one hop before the target.
6. The final install runs through the 6-step pipeline: Kill → Deps cleanup → Pip → Rebuild dirs → Write metadata → Launch.
7. If launch fails, the adapter restores from the emergency backup automatically.

Auto-update check can be toggled in CFG → CONFIGURATION.

---

## Version Scheme

```
MAJOR . BIG_UPDATE . SMALL_UPDATE . X[BUGFIX]

Example: 1.0.1.X1
  1       = major version
  0       = big update batch
  1       = small update
  X1      = second bugfix release on this version
```

---

## Contributing

Issues and pull requests are welcome. If you find a bug, open an issue with:

- V0RTEX version (shown in the bottom status bar)
- Python version (`python --version`)
- Windows version
- Crash report from `v0rtex_utils/debug_log/crash_log/`

---

## License

Copyright © 2024–2026 Vider_06. All rights reserved.  
See [LICENSE](https://github.com/Vider06/V0rtex/blob/main/LICENSE) for full terms.
