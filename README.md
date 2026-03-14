# V0RTEX v0.9.7

**V0RTEX** is a self-contained Windows malware analysis platform built in Python + Tkinter.  
`V = Vider · 0 = zero-day · R = Reverse · T = Threat · E = Engine · X = eXamine`

> **Author:** Vider_06  
> **Platform:** Windows 10/11 only · Python 3.10+ · Single file, no external launcher required  
> **License:** Copyright © 2024-2025 Vider_06 — All rights reserved. See [LICENSE](./LICENSE).

---

## Features

| Area | Details |
|------|---------|
| **YARA** | Custom rule editor with syntax highlighting · Community library downloader (Neo23x0, Elastic, Avast, VirusTotal, Yara-Rules, JPCERT/CC…) · String deobfuscator · Sigma rule viewer |
| **VirusTotal** | File scan · Hash lookup · Bulk hash batch · Auto-upload · Rescan scheduling |
| **PE Inspector** | Headers · Imports · Exports · Sections · Suspicious API detection · Entropy per section |
| **IOC** | Auto-extraction (IPs, domains, URLs, hashes, emails, CVEs, registry keys) · MITRE ATT&CK mapping · Feed import · IP/Domain reputation |
| **Sandbox** | Auto-scan watched folder · Process monitor · File analyzer · Raw string extraction · Cuckoo/CAPE integration |
| **Network** | Active connections with PID · URL tools & redirect chain · PCAP capture · Port scan · DNS · WHOIS · SSL/TLS certificate inspector · HTTP header inspector |
| **Crypto** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Vigenère · Hash inspector · Base64/Hex/XOR encoder-decoder · JWT decoder |
| **APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan · AlienVault OTX · Shodan · GreyNoise · HybridAnalysis |
| **Entropy** | File entropy chart · Section-level analysis · Verdict gauge |
| **Process** | Live process scanner · Service viewer · Startup items · Environment variables · Open file handles · Process tree |
| **Lookup** | Quick hash · Bulk hash · Strings · File diff · Extract IOC · Regex · Archive inspector · Macro analyzer · Document analyzer · Binary pattern search · Number base converter · Unicode inspector · PE header viewer |
| **Notes** | Scratchpad · MITRE map · TODO task list · Snippet library · Report builder |
| **Defense** | Real-time watchdog · Quarantine · Self-defense · App integrity · Folder protection · Auto-backup |
| **Crypto Tools** | Encrypt/decrypt files · Inspect encryption state · Compute hashes |
| **DB** | SQLite · Full scan history · Export CSV/JSON/HTML · Scan history browser |

**21 main tabs · 80+ sub-tabs**

---

## Installation

### Requirements
- Windows 10 or 11 (64-bit)
- Python 3.10 or higher → [python.org](https://www.python.org/downloads/)
- Internet connection (for API lookups and rule downloads)
- Administrator rights recommended for first launch

### Steps

1. **Clone or download** this repository:
```
   git clone https://github.com/Vider06/V0rtex.git
```

2. **Run the file** — the built-in setup wizard launches automatically on first start:
```
   python v0rtex.py
```

3. **Follow the setup wizard** — it will automatically:
   - Install all required Python packages via `pip`
   - Install **Microsoft C++ Build Tools** (required to compile `yara-python`)
   - Download and install Wireshark/tshark (optional, for network capture)
   - Create the full folder structure (`rules/`, `reports/`, `backups/`, `external/`, `debug_log/`)
   - Write `config.json`, `whitelist.txt`, `notes.txt` with factory defaults
   - Create `scan_history.db` (SQLite)
   - Compile YARA rules in the background after launch

4. **Configure API keys** → `CFG` tab → `API KEYS` — paste your keys for:
   - VirusTotal, MalwareBazaar, AbuseIPDB, URLScan, AlienVault OTX, Shodan, GreyNoise, HybridAnalysis

5. **Download YARA rule libraries** → `YARA` tab → `LIBRARY` — select repos and click **DOWNLOAD**.

> ⚠ **Run as Administrator** on first launch for full process/network monitoring functionality.

---

## Quick Guide

### Scanning a file
1. Drag and drop a file onto the main window **or** click **+ Add File**
2. V0RTEX runs in sequence: YARA scan → PE parsing → entropy → IOC extraction → VirusTotal lookup (if key set)
3. Results appear on the **HOME** dashboard and are saved to the local SQLite database
4. Click any row in RECENT SCANS to open the full scan report

### YARA Rule Manager
- **YARA → LIBRARY**: download community rule sets from GitHub. Supported repos: Neo23x0, Elastic Security, Avast Threat Intel, VirusTotal, Yara-Rules, JPCERT/CC, mikesxrs
- **YARA → RULE EDITOR**: write and test custom `.yar` rules with syntax highlighting, compile check and live file test
- **YARA → DEOBF**: deobfuscate strings found in YARA hits
- **YARA → SIGMA**: load `.yml` Sigma rules and inspect detection logic and metadata
- Rules are auto-compiled at startup and after every download

### Process Sandbox
- **SB → AUTO-SCAN**: set a watch folder — any new file dropped is automatically queued and scanned
- **SB → PROCESS**: inspect running processes, send suspicious EXEs directly to YARA, kill processes
- **SB → FILE ANALYZER**: deep static analysis of a single file
- **SB → STRING EXTRACT**: extract raw ASCII and Unicode strings from any binary

### Network Monitor
- **NET → CONNECTIONS**: live view of all active connections with PID and process name (requires admin)
- **NET → PCAP**: start/stop packet capture via tshark, save to file
- **NET → PORT SCAN**: scan a host for open ports
- **NET → DNS**: query A, AAAA, MX, TXT, NS, CNAME, PTR records
- **NET → WHOIS**: WHOIS lookup for domains and IPs
- **NET → URL TOOLS**: follow redirect chains, expand short URLs
- **NET → IP/DOMAIN REP.**: query VirusTotal + AbuseIPDB + ipinfo.io in bulk

### IOC Extractor
- **IOC → EXTRACT IOC**: paste text or load a file — auto-extracts IPs, domains, URLs, hashes, emails, CVEs, registry keys
- **IOC → MITRE**: map extracted IOCs and suspicious APIs to MITRE ATT&CK techniques
- **IOC → FEED**: import threat feeds (CSV/JSON/TXT) into the local database
- Results can be exported or sent directly to the reputation query tool

### Defense Mode
- **PROT tab**: enables real-time monitoring of the V0RTEX install folder, detects tampering and auto-quarantines threats
- **WD tab**: monitors any user-defined folder for new files and auto-queues them for scanning

---

## Recovery UI

V0RTEX has a built-in **Recovery UI** that activates automatically when critical files are missing or corrupted at startup.

### When it triggers
- One or more embedded module files are missing from the install directory
- `config.json` is corrupted or unreadable
- `scan_history.db` is missing or has an invalid schema

### What it does

| Action | Description |
|--------|-------------|
| **Recreate Critical Files & Dirs** | Re-extracts all embedded files (modules, config, DB schema, whitelist, notes) from the script itself |
| **Reset config.json** | Writes factory-default configuration, preserving API keys if possible |
| **Repair DB Schema** | Recreates missing tables in `scan_history.db` without deleting existing scan records |
| **Restore from Backup** | Imports a `.zip` backup created by V0RTEX's backup system |
| **Diagnostics** | Runs a full dependency check, YARA rule validation and network connectivity test |
| **Clean** | Removes orphaned temp files, empty log folders and stale lock files |
| **Network Test** | Verifies internet access and VirusTotal API reachability |

### How to use it
If V0RTEX closes immediately after launch, run from terminal:
```
python v0rtex.py
```
If the Recovery UI appears, click **Recreate Critical Files & Dirs** first — this resolves 90% of startup issues. Then click **Repair DB Schema** and restart normally. If the issue persists, use **Restore from Backup** and select a `.zip` from the `backups/` folder.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **Window opens and immediately closes** | Run from terminal (`python v0rtex.py`) — check the error. If the Recovery UI appears, use **Recreate Critical Files** |
| **`KeyError` on startup** | Corrupt `config.json` — delete it from the install folder and restart, or use Recovery UI → Reset config |
| **`Invalid column index` crash** | Download the latest `v0rtex.py` from the repo |
| **YARA not working / disabled** | `yara-python` requires Microsoft C++ Build Tools — installed automatically by setup. If skipped: `winget install Microsoft.VisualStudio.2022.BuildTools` then `pip install yara-python` |
| **VirusTotal returns no results** | Check API key in CFG → API KEYS. Free tier: 500 requests/day |
| **tshark / network capture missing** | Install Wireshark from [wireshark.org](https://www.wireshark.org/) and ensure it is in PATH |
| **Setup crashes with admin error** | Right-click `v0rtex.py` → *Run as administrator* |
| **YARA rules download 0 files** | Some repos (e.g. Avast) use per-family subdirectories — place `.yar`/`.yara` files manually in `rules/` |
| **High memory on startup** | Background YARA compile is running — wait 30–60 seconds |
| **Recovery UI appears every launch** | A module file is being deleted by antivirus — add the install folder to Windows Defender exclusions (done automatically by setup) |
| **Crash report window appears** | Check `debug_log/` for `crash_log.txt` — contains full traceback |

---

## Folder Structure
```
V0rtex_System/
└── V0RTEX_v0.9/
    ├── v0rtex.py          ← the application
    ├── config.json        ← all settings
    ├── scan_history.db    ← SQLite scan database
    ├── whitelist.txt      ← hash/path exclusions
    ├── notes.txt          ← scratchpad
    ├── rules/             ← YARA rule files (.yar / .yara)
    ├── reports/           ← generated HTML/PDF/JSON reports
    ├── modules/           ← embedded helper modules
    ├── debug_log/         ← session logs and crash reports
    └── backups/           ← auto-created backup ZIPs
```

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
