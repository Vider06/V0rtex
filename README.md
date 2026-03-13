# V0RTEX v1.0

**V0RTEX** is a self-contained Windows malware analysis platform built in Python + Tkinter.  
`V = Vider · 0 = zero-day · R = Reconnaissance · T = Threat · E = Engine · X = eXtract`

> **Author:** Vider_06  
> **Platform:** Windows only · Python 3.10+ · Single file, no install required  
> **License:** Copyright © 2024-2025 Vider_06 — All rights reserved. Redistribution and resale strictly prohibited. See [LICENSE](./LICENSE).

---

## Features

| Area | Details |
|------|---------|
| **YARA** | Custom rule editor · Community library downloader (Neo23x0, Elastic, Avast, VirusTotal…) · Deobfuscator |
| **VirusTotal** | File scan · Hash lookup · Bulk mode · Auto-upload |
| **PE Inspector** | Headers · Imports · Exports · Sections · Suspicious API detection |
| **IOC** | Auto-extraction · MITRE ATT&CK mapping · Feed import · IP/Domain reputation |
| **Sandbox** | Auto-scan watched folder · Process monitor · File analyzer · Cuckoo integration |
| **Network** | Active connections · URL tools · PCAP capture · Port scan · DNS · WHOIS |
| **Crypto** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Vigenère · Hash inspector |
| **APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan · AlienVault · Shodan · GreyNoise · HybridAnalysis |
| **Entropy** | File entropy chart · Section-level analysis |
| **Notes** | Scratchpad · MITRE map · TODO · Snippets |
| **Defense** | Quarantine · Real-time watchdog · Self-defense · App integrity |
| **DB** | SQLite · full scan history · export CSV/JSON/HTML |

**21 main tabs · 80+ sub-tabs**

---

## Installation

### Requirements
- Windows 10/11
- Python 3.10 or higher → [python.org](https://www.python.org/downloads/)
- Internet connection (for API lookups and rule downloads)

### Steps

1. **Clone or download** this repository:
```
   git clone https://github.com/Vider_06/v0rtex.git
```

2. **Run the file** — the built-in setup wizard launches automatically on first start:
```
   python v0rtex.py
```

3. **Follow the setup wizard** — it will automatically:
   - Install all required Python packages (`pip`)
   - Install Microsoft C++ Build Tools (required for `yara-python`)
   - Download and install Wireshark/tshark (optional, for network capture)
   - Create the folder structure (`rules/`, `reports/`, `backups/`, `external/`)
   - Compile YARA rules in the background

4. **Configure API keys** → `CFG` tab → `API KEYS` — paste your keys for:
   - VirusTotal, MalwareBazaar, AbuseIPDB, URLScan, AlienVault OTX, Shodan, GreyNoise, HybridAnalysis

5. **Download YARA rule libraries** → `YARA` tab → `LIBRARY` — select repos and click **DOWNLOAD**.

> ⚠ **Run as Administrator** on first launch for full process/network monitoring functionality.

---

## Quick Guide

### Scanning a file
1. Drag and drop a file onto the main window **or** click **DROP FILE HERE**
2. V0RTEX runs: YARA scan → PE parsing → entropy → IOC extraction → VirusTotal lookup (if key set)
3. Results appear on the **HOME** dashboard and are saved to the local SQLite database

### YARA Rule Manager
- **YARA tab → LIBRARY**: download community rule sets from GitHub (Neo23x0, Elastic, Avast, VirusTotal, Yara-Rules, JPCERT/CC…)
- **YARA tab → EDITOR**: write and test custom rules directly in the UI
- Rules are auto-compiled at startup and on every download

### Process Sandbox
- **SB tab → AUTO-SCAN**: set a watch folder — any new file dropped is automatically queued and scanned
- **SB tab → PROCESS**: inspect running processes, send suspicious EXEs directly to YARA

### Network Monitor
- **NET tab → CONNECTIONS**: live view of all active connections with PID/process name (requires admin)
- **NET tab → PCAP**: start/stop packet capture via tshark

### IOC Extractor
- **LOOK tab → EXTRACT IOC**: paste or load text — extracts IPs, domains, URLs, hashes, email addresses
- Results can be exported or pushed directly to the reputation query tool

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| **Window opens and immediately closes** | Run from terminal (`python v0rtex.py`) and check the error — usually a missing package. Re-run setup or `pip install -r requirements.txt` |
| **`KeyError` on startup** | Corrupt or outdated `config.json` — delete it from the install folder and restart |
| **YARA not working / disabled** | `yara-python` requires Microsoft C++ Build Tools — installed automatically by the setup wizard. If skipped, run: `winget install Microsoft.VisualStudio.2022.BuildTools` then reinstall `yara-python` |
| **VirusTotal returns no results** | Check API key in CFG → API KEYS. Free tier limit: 500 requests/day |
| **tshark / network capture missing** | Install Wireshark from [wireshark.org](https://www.wireshark.org/) and ensure it is in PATH |
| **Setup crashes with admin error** | Right-click `v0rtex.py` → *Run as administrator* |
| **YARA rules download 0 files** | Some repos (e.g. Avast) use per-family subdirectories — place `.yar`/`.yara` files manually in the `rules/` folder |
| **High memory usage on startup** | Background YARA compile is running — wait 30–60 seconds |

---

## Dependencies

Installed automatically by the setup wizard:
```
requests · psutil · pefile · yara-python · pywin32 · Pillow
cryptography · scapy · python-whois · dnspython
```

Also installed automatically:
- **Microsoft C++ Build Tools** — required to compile `yara-python` from source
- **Wireshark/tshark** — network capture (optional, prompted during setup)

---

## License

Copyright © 2024-2025 Vider_06 — All rights reserved.  
Redistribution, resale, and repackaging are strictly prohibited.  
See [LICENSE](./LICENSE) for full terms.
