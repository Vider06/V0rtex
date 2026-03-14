# V0RTEX v0.9.7.X3

**V0RTEX** is a self-contained Windows malware analysis platform built in Python + Tkinter.  
`V = Vider · 0 = zero-day · R = Reverse · T = Threat · E = Engine · X = eXamine`

> **Author:** Vider_06  
> **Platform:** Windows 10/11 only · Python 3.10+ · Single file, no external launcher required  
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
| **Notes** | Scratchpad · MITRE map · TODO list · Snippet library · Report builder |
| **Defense** | Real-time watchdog · Quarantine · Self-defense · App integrity · Folder protection · Auto-backup |
| **DB** | SQLite · Full scan history · Export CSV/JSON/HTML · Scan history browser |

**21 main tabs · 80+ sub-tabs**

---

## Installation

### Requirements
- Windows 10 or 11 (64-bit)
- Python 3.10 or higher → [python.org](https://www.python.org/downloads/)
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
   - Installs **Microsoft C++ Build Tools** (required for `yara-python`)
   - Downloads and installs Wireshark/tshark (optional)
   - Creates the full folder structure
   - Writes `config.json`, `whitelist.txt`, `notes.txt` with factory defaults
   - Creates `scan_history.db`
   - Compiles YARA rules in the background after launch

4. **Configure API keys** → `CFG` tab → `API KEYS`

5. **Download YARA rules** → `YARA` tab → `LIBRARY` → select repos → **DOWNLOAD**

> ⚠ **Run as Administrator** on first launch for full process/network monitoring.

---

## Folder Structure
```
V0rtex_System/
├── V0RTEX_v0.9.7.X3/               ← main install directory (BASE_DIR)
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

## What's new in v0.9.7.X3

- **Updater fix** — version comparator now correctly handles alphanumeric version tags (`X1`, `X2`, `X3`…). Previously the updater always reported "up to date" due to a `int()` parse failure on non-numeric version parts.
- **Dual-file update** — the updater now also patches the external launcher (`v0rtex.py` outside `V0rtex_System`) if one is detected. If the running file is already the app copy, it searches parent directories automatically and shows a popup to confirm or browse manually.
- **Reinstall — local copy default** — reinstall no longer downloads from GitHub by default. It copies the currently running script to TEMP, then launches setup. An optional checkbox `⬇ Download latest from GitHub` enables remote fetch with automatic fallback to local copy on failure. The temp file is deleted automatically after launch.
- **Recovery REPAIR tab** — new **🧹 Clean TEMP** button removes all V0RTEX-related temp files (`v0rtex_fresh_install*.py`, trampolines, `vs_buildtools_setup*.exe`, `get-pip*.py`).
- **Crash UI fix** — corrected ASCII X art (line 4 had a stray `╔` box character).

---

## Main UI — Tab Reference

### 🏠 HOME
The main dashboard. Shows live scan statistics (total scans, malicious, clean, YARA hits, queue, API keys), a threat level bar, and the recent scans table. The right panel contains **Quick Actions** (Add File, Add Folder, Scan URL, Sandbox, AutoScan, Watch Folder) and **V0RTEX INFO** (build info, version, APIs). Clicking any row in the recent scans table opens the full scan report popup.

### 📋 LOGS
Three log panels in a scrollable view: **FILE OPERATIONS** (every scan event with verdict), **DEBUG LOG** (internal checkpoints, errors, background thread activity). Logs are also written to `debug_log/` on disk. A clear button and export to `.txt` are available.

### 📊 CHRT (Charts)
Three sub-tabs:
- **Charts** — live bar/pie charts of scan results (malicious vs clean vs YARA), updated after each scan. A Refresh button forces a redraw.
- **ENT** — entropy distribution histogram across all scanned files.
- **HEAT** — heatmap of threat categories vs file types across all scanned samples.

### 📁 REP (Reports)
Browse, open and delete scan reports. Supports HTML, JSON and plain text formats. Double-click a report to open it in the built-in viewer or in the default browser. Diff view compares two reports side by side to detect changes between scans of the same file.

### 🎯 IOC
Four sub-tabs:
- **IOC** — automatic IOC extraction from scan results. Extracts IPs, domains, URLs, MD5/SHA hashes, email addresses, CVEs, registry keys and Windows API names.
- **MITRE** — maps extracted IOCs and suspicious API calls to MITRE ATT&CK techniques and tactics with description and links.
- **Feed** — import external threat feed files (CSV, JSON, TXT) into the local database for enrichment.
- **IP/Domain Rep.** / **Stats** / **Export** — bulk reputation lookup and IOC export.

### 🛡 YARA
Five sub-tabs:
- **YARA** — main scan controls: run YARA against any file, view hits with rule name, namespace and matched strings.
- **LIBRARY** — download community rule sets from GitHub. Select any combination of: Neo23x0 (Florian Roth), Elastic Security, Avast Threat Intel, VirusTotal, Yara-Rules (malware/crypto/packers/RATs/CVE/email/maldocs/webshells), JPCERT/CC, mikesxrs. Shows download status, file count and per-rule validation.
- **✏ RULE EDITOR** — full in-editor YARA rule authoring with syntax highlighting (keywords, modifiers, strings, hex patterns, comments). Compile & Test compiles the rule and reports errors. Test on File runs the compiled rule against any chosen file and shows matches. Save/Open rules directly to/from `rules/`.
- **DEOBF** — string deobfuscator. Paste obfuscated content from a YARA hit and run XOR brute-force, base64 decode, ROT variants and hex decode automatically.
- **Σ SIGMA** — load `.yml` Sigma detection rules. Displays rule metadata (title, status, author, date, tags), detection logic (keywords, conditions), and the mapped MITRE techniques.

### ⚡ PERF
System performance monitor. Tracks CPU%, RAM (used/total), disk I/O and network I/O. Updates every 5 seconds. Shows per-process CPU/memory breakdown for python processes. Useful for diagnosing V0RTEX resource usage during heavy scans.

### ⏱ TL (Timeline)
Chronological scan history chart. Plots scan events on a time axis showing verdict (malicious/clean/YARA), file type and entropy. Helps identify scan patterns and time-correlated threat activity.

### 🔬 SB (Sandbox)
Four sub-tabs:
- **Auto-Scan** — folder watcher. Set a directory and V0RTEX automatically queues any new file dropped into it for full analysis. Shows watcher status, queue depth and last event.
- **Process** — live running process list with PID, name, CPU%, memory, command line. Suspicious process names are highlighted in red. Right-click to send the process EXE directly to YARA or kill the process.
- **File Analyzer** — deep static analysis of a single chosen file: magic bytes, file type, entropy, PE info, embedded strings, IOC extraction, YARA scan, all in one view.
- **String Extract** — extract raw ASCII and Unicode strings from any binary with configurable minimum length and encoding filter.

### 🏗 SETUP
First-time setup and reinstall wizard. Accessible from the main UI for re-running installation steps without restarting. Can repair packages, re-extract embedded modules, reset config and verify the full installation state.

### 👁 WD (Watchdog)
Independent folder monitor. Monitors any user-defined path for file creation, modification and deletion events. Logs all activity in real time. Can be configured to auto-quarantine suspicious new files or to just alert. Independent of the SB Auto-Scan watcher.

### ⚙ CFG (Config)
Six sub-tabs:
- **API KEYS** — paste API keys for all supported services. Inline test button verifies each key immediately.
- **CONFIGURATION** — rate limit, tshark path, proxy, timeouts, scan behaviour (recursive, skip empty, auto-report format, hash priority).
- **WHITELIST** — hash and path exclusions. Files matching an entry are skipped during scanning.
- **EXPORT** — export scan history to CSV, JSON or HTML. Configurable date range and verdict filter.
- **🔖 CHECKPOINT** — real-time log of all internal debug checkpoints for the current session. Also written to `debug_log/`. Export to `.txt`.
- **SCAN HISTORY** — browse all past scans stored in `scan_history.db`. Filter by date, verdict, file type. Double-click to view full details.
- **DEBUG LOG** — browse and search debug log files from `debug_log/`.
- **REPORT BUILDER** — compose a custom Markdown investigation report with pre-filled sections (summary, IOCs, YARA hits, timeline, notes). Export to `.md`.
- **🔄 UPDATER** — check for new versions on GitHub and apply updates automatically.

### 🔎 LOOK (Lookup)
Fifteen sub-tabs covering every static analysis and encoding tool:
- **Hash** — three nested tabs: **Quick Hash** (single hash VT lookup), **Bulk Hash** (batch hash list against VirusTotal), **Strings** (extract and search strings), **Diff** (file diff analyzer: hash diff, size diff, hex diff, text diff), **Extract IOC** (paste text and extract all IOC types).
- **HEX** — full hex viewer and binary inspector with search, offset navigation and ASCII panel.
- **REGEX** — regex workbench. Test patterns against text with match highlighting.
- **DOC** — document analyzer for PDF and Office files. Extracts metadata, embedded objects, macros, URLs and IOCs.
- **SIG** — Authenticode signature verifier for PE executables. Shows subject, issuer, validity dates, trust chain and hash.
- **BATCH** — bulk file hash batch processor.
- **DIFF** — standalone file diff with side-by-side compare and Export HTML.
- **ARCHIV** — archive inspector (ZIP, RAR, 7z). Lists contents, extracts files, scans entries.
- **MACRO** — Office macro analyzer. Extracts and decompiles VBA macros, flags suspicious API calls and IOCs.
- **B64** — Base64/Hex/Base32 encoder-decoder.
- **XOR** — XOR encoder-decoder with byte/string key.
- **BCONV** — number base converter (binary/octal/decimal/hex).
- **JWT** — JWT decoder. Inspects header, payload, expiry and signature.
- **ROT** — ROT13, ROT47 and Caesar cipher with custom shift and brute-force all 25 values.
- **PE-HDR** — PE header viewer. Displays DOS header, NT headers, section table, imports and exports in a structured tree.
- **UNICODE** — Unicode inspector. Code points, URL encode/decode, HTML entities, encoding detection.
- **BINPAT** — binary pattern search. Search hex patterns, magic bytes or ASCII signatures in any binary file.

### 🖥 PROC (Processes)
Six sub-tabs:
- **Processes** — live process list with full details (PID, PPID, name, CPU%, memory, command line). Highlight suspicious processes.
- **Services** — list all Windows services with status, start type and binary path.
- **Startup Items** — enumerate Run/RunOnce registry keys and Startup folders for persistence mechanisms.
- **Env Variables** — display all environment variables for the current session.
- **Handles** — list files opened by all running processes via psutil. Filter by PID.
- **🌳 Proc Tree** — hierarchical parent-child process tree. Useful for detecting process injection and anomalous spawning.
- **🗝 Registry** — registry scanner. Browse and search registry keys for suspicious entries.

### 🌐 NET (Network)
Seven sub-tabs:
- **Connections** — live view of all active TCP/UDP connections with PID, process name, local and remote address, state.
- **URL Tools** — follow redirect chains, expand short URLs, detect malicious redirects.
- **🕵 IP/Domain Rep.** — bulk query VirusTotal + AbuseIPDB + ipinfo.io for any IP, domain or URL.
- **DNS** — query A, AAAA, MX, TXT, NS, CNAME and PTR records for any hostname.
- **WHOIS** — WHOIS lookup via socket on port 43 for domains and IPs.
- **HTTP Header Inspector** — fetch response headers for any URL. Checks for missing security headers (HSTS, CSP, X-Frame-Options, etc.).
- **SSL/TLS Certificate Inspector** — fetch and display X.509 certificate details for any HTTPS host (subject, issuer, validity, SANs, fingerprint).
- **🔌 Port Scan** — TCP port scanner with configurable range and timeout.
- **PCAP** — start/stop packet capture via tshark. Save to `.pcap` file, then analyze with the built-in PCAP analyzer.

### 📝 NOTES
Four sub-tabs:
- **Notepad** — persistent scratchpad. Content is auto-saved to `notes.txt` on every keystroke.
- **MITRE ATT&CK** — interactive MITRE ATT&CK technique mapper. Add techniques manually or import from scan results. Export as Markdown or JSON.
- **TODO** — investigation task list with priority levels and status tracking. Auto-saved to disk.
- **Snippets** — snippet library. Save frequently used commands, regex patterns and IOC templates. Add, edit, delete and copy to clipboard.

### ⚙ SET (Global Settings)
Nine sub-tabs covering all configurable parameters:
- **Interface** — font size, log max lines, confirm-on-exit, tray behaviour, splash screen, status animation, toast duration.
- **Scan** — max file size, VT request delay, timeout, auto-upload, auto-YARA compile, auto-report, report format, hash priority, recursive scan, skip empty files, save IOCs automatically, compare with previous scan, notify on malicious/clean.
- **Privacy** — log and DB retention days, store/anonymize file paths and hashes.
- **Paths** — custom paths for rules, reports, debug log, quarantine and backups.
- **Network** — proxy URL/auth, request timeout, max retries, VT rate limit, custom user-agent, PCAP capture duration, DNS timeout.
- **Defense** — auto-quarantine threshold, auto-delete malicious, mal threshold, deep scan mode, scan archives, entropy threshold, YARA timeout, sandbox duration, VT after sandbox, block execution, real-time protect.
- **Notifications** — toast, tray, sound alerts. Per-event toggles (malicious, suspicious, scan done, YARA hit, crash). Duration and optional email/SMTP alerts.
- **Advanced** — max queue size, debug mode, log performance, GC mode (gen0/gen1/full), checkpoint verbosity.
- **Automatic Actions** — auto-actions triggered by scan verdicts (quarantine, alert, run script).

### 🔒 PROT (App Protection)
Five sub-tabs:
- **🏗 Build/Destroy** — create or teardown the V0RTEX protected environment. Builds integrity baseline, registers self-defense hooks.
- **Protected Folders** — define folders that V0RTEX monitors for unauthorized changes.
- **Integrity** — compute and verify file hashes for all critical V0RTEX files to detect tampering. Shows modified/missing count.
- **🛡 Defense** — arm/disarm the real-time defense engine. When armed, monitors the install folder and auto-quarantines threats.
- **Self-Defense** — protects the V0RTEX process itself from being killed or tampered with by external processes.
- **💾 Backup** — create full lab ZIPs (script + config + rules + DB). Auto-restore if a backup is found on startup.

### 🔐 CRYPT (Crypto)
Five sub-tabs:
- **🔒 Encrypt** — encrypt files or text using AES-256-GCM, RSA or Vigenère. Password-based with salt and IV.
- **🔓 Decrypt** — decrypt `.soc_enc` files produced by V0RTEX. Auto-detects algorithm.
- **🔍 Inspect** — drop or select any file to detect its encryption state, compute hashes and verify integrity.
- **🔏 Hash** — generate and verify MD5/SHA-1/SHA-256/SHA-512/CRC32 from text or file input.
- **🔡 Vigenère** — polyalphabetic cipher encoder/decoder with a keyword.

### ⚠ DZ (Danger Zone)
Collection of powerful destructive and diagnostic tools requiring deliberate use. Includes:
- **Clear Logs** — wipe all debug and operation logs.
- **Factory Reset** — delete all data (DB, reports, YARA rules, config, logs, whitelist). Irreversible.
- **Secure Wipe** — overwrite files with zeros before deletion.
- **System Info** — display system paths, Python info, installed packages and resource usage.
- **Open Log Folder** — open `debug_log/` in Explorer.
- Various low-level diagnostic and cleanup utilities.

---

## Recovery UI

V0RTEX has a built-in **Recovery Terminal** that activates automatically when critical files are missing or corrupted at startup, or when a crash is detected before the main UI can load.

### When it triggers
- One or more embedded module files (`modules/pe_analysis.py`, `modules/cuckoo_api.py`, `modules/secret_scanner.py`, `modules/wireshark.py`) are missing from `BASE_DIR`
- `config.json` is corrupted, unreadable or has invalid JSON
- `scan_history.db` is missing or has a broken schema
- An unhandled exception occurs before the main window is displayed

### Structure of the Recovery Terminal

The Recovery Terminal is a fully independent Tkinter window with its own notebook containing six tabs:

#### >_ Terminal
A fully functional embedded command shell. Type any Windows shell command directly. Includes a **QUICK CMDS** panel with one-click shortcuts for the most common recovery operations (`pip list`, `python --version`, `dir`, `netstat`, etc.). The prompt shows the current working directory and updates after `cd` commands. Output is color-coded (stdout, stderr, system messages).

#### 💥 Crash Log
Displays the full crash log from the last session if one exists. Shows exception type, traceback with file and line numbers, Python version, platform and PID. Includes buttons to **Copy** the full log to clipboard and **Open Log Folder** in Explorer. If no crash log is present, shows the message `No crash log found`.

#### 📋 File Check
Scans the V0RTEX install directory and verifies the presence and integrity of all expected files: `v0rtex.py`, `config.json`, `scan_history.db`, `whitelist.txt`, `notes.txt`, `requirements.txt`, all `modules/` files, `rules/` directory, `reports/` directory, `debug_log/` directory and `backups/` directory. Each entry shows ✓ present or ✗ missing. Buttons: **Run Check**, **Copy Results**.

#### 🔧 Repair
The main recovery workhorse. Contains these repair actions:

| Button | What it does |
|--------|-------------|
| **Recreate Critical Files & Dirs** | Re-extracts all embedded files from the script (modules, config, DB schema, whitelist, notes, requirements.txt, `launch.bat`). Creates missing directories. This is the first action to try for any startup failure. |
| **Reset config.json** | Writes factory-default `config.json`. Attempts to preserve existing API keys by reading the broken file first. |
| **Repair DB Schema** | Opens `scan_history.db` and recreates any missing tables or columns without touching existing scan records. Safe to run even on a partially healthy database. |
| **Install / Repair Packages** | Runs a full pip install cycle for all required packages with multiple fallback strategies: bulk install → per-package → `--user` → system Python fallback. Also attempts to install Microsoft C++ Build Tools if `yara-python` fails. |
| **Restore from Backup** | Opens a file picker to select a V0RTEX backup `.zip`. Extracts config, database, rules, whitelist and notes into `BASE_DIR`. Does not overwrite `v0rtex.py` unless explicitly included in the backup. |
| **🧹 Clean TEMP** | Removes all V0RTEX-related temp files left by the installer, reinstall wizard or trampoline scripts (`v0rtex_fresh_install*.py`, `v0rtex_*_trampoline*.py`, `vs_buildtools_setup*.exe`, `get-pip*.py`). |

All repair actions stream their output live to the log panel on the left side of the tab.

#### 💾 Backup
Create a new backup ZIP from the current state of the install directory. The backup includes `v0rtex.py`, `config.json`, `scan_history.db`, `whitelist.txt`, `notes.txt` and the entire `rules/` folder. Saved to `backups/` with a timestamp. Also lists existing backups with size and date.

#### 🩺 Diagnostics
Runs automated checks across four areas:

| Check | Description |
|-------|-------------|
| **Dependency Check** | Imports every required package and reports version. Flags missing or broken packages with install suggestions. |
| **YARA Rules** | Compiles all `.yar`/`.yara` files in `rules/` and `rules/external/`. Reports syntax errors per file with line numbers. |
| **Running Processes** | Lists all Python processes currently running to detect stuck V0RTEX instances. |
| **Network** | Tests internet connectivity, resolves DNS for `8.8.8.8`, checks VirusTotal API reachability if a key is configured. |

#### 🧹 Clean
Removes orphaned and temporary files: stale `_v0rtex_relaunch.py` trampoline files, empty log directories, `__pycache__` folders, `.pyc` files and leftover temp install scripts.

#### 🌐 Network
Quick network test panel. Checks general internet connectivity, DNS resolution, proxy configuration and VirusTotal API access. Results shown in color-coded output with latency measurements.

### How to use the Recovery Terminal

**Scenario 1 — V0RTEX closes immediately:**
```
python v0rtex.py
```
If the Recovery Terminal appears, go to **🔧 Repair** → click **Recreate Critical Files & Dirs**. Wait for the log to show all ✓. Then click **Repair DB Schema**. Close the Recovery Terminal and relaunch.

**Scenario 2 — YARA disabled at every launch:**
Go to **🔧 Repair** → **Install / Repair Packages**. The installer will attempt to compile `yara-python` with Build Tools. If Build Tools are missing it will install them automatically (requires internet and ~5–15 minutes).

**Scenario 3 — config.json corrupted:**
Go to **🔧 Repair** → **Reset config.json**. Your API keys will be preserved if the JSON was partially readable.

**Scenario 4 — Database errors:**
Go to **🔧 Repair** → **Repair DB Schema**. This recreates missing tables without deleting scan history.

**Scenario 5 — Unknown crash:**
Go to **💥 Crash Log**, copy the full traceback, and open a GitHub Issue with it.

**Scenario 6 — Leftover temp files after reinstall:**
Go to **🔧 Repair** → **🧹 Clean TEMP** to remove any installer temp files left in the system TEMP folder.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **Window opens and immediately closes** | Run from terminal (`python v0rtex.py`). If Recovery Terminal appears use **Recreate Critical Files** |
| **`KeyError` on startup** | Corrupt `config.json` — Recovery Terminal → Reset config.json |
| **`Invalid column index` crash** | Download the latest `v0rtex.py` from the repo |
| **YARA not working / disabled** | Recovery Terminal → Install / Repair Packages. Or manually: `winget install Microsoft.VisualStudio.2022.BuildTools` then `pip install yara-python` |
| **VirusTotal returns no results** | CFG → API KEYS — verify key. Free tier: 500 requests/day |
| **tshark / network capture missing** | Install Wireshark from [wireshark.org](https://www.wireshark.org/) and ensure it is in PATH |
| **Setup crashes with admin error** | Right-click `v0rtex.py` → *Run as administrator* |
| **YARA rules download 0 files** | Some repos (e.g. Avast) use per-family subdirectories — place `.yar`/`.yara` files manually in `rules/` |
| **High memory on startup** | Background YARA compile is running — wait 30–60 seconds |
| **Recovery Terminal appears every launch** | Antivirus is deleting module files — add the install folder to Windows Defender exclusions (done automatically by setup) |
| **Crash report window on every launch** | Check `debug_log/crash_log.txt` for the traceback and open a GitHub Issue |
| **Updater says "up to date" on old version** | Update to v0.9.7.X3 — earlier versions had a version comparison bug with alphanumeric tags |

---

## Dependencies

Installed automatically by the setup wizard:
```
requests · psutil · pefile · yara-python · pywin32 · Pillow
cryptography · scapy · python-whois · dnspython · matplotlib
tkinterdnd2 · fpdf2 · watchdog · pystray · reportlab
```

Also installed automatically:
- **Microsoft C++ Build Tools** — required to compile `yara-python` from source
- **Wireshark/tshark** — network capture (optional, prompted during setup)

---

## License

Copyright © 2024-2025 Vider_06 — All rights reserved.  
Redistribution, resale, and repackaging are strictly prohibited.  
See [LICENSE](./LICENSE) for full terms.

If you are reading this... Why would you EVER read all of this dude
Alr, try it and report me bugs or anything tbh - Vider_06
