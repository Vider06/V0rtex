# V0RTEX

> `V = Vulnerability · O = Oriented · R = Recon · T = Threat · E = Exploitation · X = eXaminer`

**V0RTEX** is an open-source, single-file Windows malware analysis platform built in Python + Tkinter.  
One script. No installer required beyond running `python v0rtex.py`.

**Author:** Vider_06  
**Platform:** Windows 10 / 11 (64-bit)  
**Python:** 3.10 or higher — including 3.12, 3.13, 3.14  
**License:** Copyright © 2024–2026 Vider_06. All rights reserved. See [LICENSE](LICENSE).

---

## What is V0RTEX?

V0RTEX is a complete malware analysis lab inside a single Python script (~35,000 lines). It covers the full analysis workflow — from initial triage and static analysis through dynamic monitoring and post-analysis reporting — and includes network privacy tools, a self-protection layer, a trampoline-based auto-updater, and a full Windows system health checker.

It is designed for malware analysts, SOC operators, and security researchers who want a self-contained environment with no cloud dependency and no external launcher.

---

## Features at a Glance

| Area | Highlights |
|---|---|
| **Static Analysis** | Hashes · PE headers · Imports/Exports · Strings · Entropy · Sections · Suspicious API detection · IMPHASH |
| **YARA** | Custom rule editor · Community library downloader · yara-python / yara-x multi-engine · Deobfuscator · Sigma viewer |
| **IOC** | Auto-extraction · MITRE ATT&CK mapping · Feed import · Reputation · Secrets scanner |
| **Network** | Live connections · PCAP · Port scan · DNS · WHOIS · SSL/TLS · Proxy · Tor · Noise generator · Live traffic · Connection stats |
| **VirusTotal** | File scan · Hash lookup · Bulk batch · URL scan |
| **Threat APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan · AlienVault OTX · Shodan · GreyNoise · HybridAnalysis |
| **Sandbox** | Auto-scan drop folder · Process monitor · File analyzer · Cuckoo/CAPE integration |
| **Crypto / Encoding** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Base64/Hex/XOR · JWT · ROT · Vigenère |
| **Lookup** | HEX · REGEX · DOC · SIG · DIFF · Archive · Macro · B64 · XOR · PE-HDR · Unicode · BinPat · Fuzzy hash |
| **Process** | Live scanner · Services · Startup items · Env variables · Handles · Process tree · Registry browser |
| **Defense** | Real-time watchdog · Quarantine · Self-defense · Integrity check · Folder protection · Auto-backup · Emergency rollback |
| **Privacy** | Log censor · Auto-censor toggle · Per-category rules · Temp log storage management |
| **System Check** | Defender status · SFC · DISM · Disk SMART · Startup persistence · System Fixer · Full deep scan |
| **Updater** | Adapter-based pipeline · Trampoline chain for large version gaps · Self-updating adapter · Fresh install / data reset modes |

**21 main tabs · 90+ sub-tabs**

---

## Branches

This repository uses separate branches for active development and platform-specific releases.

| Branch | Description |
|---|---|
| `main` | This overview, changelog, and stable release files |
| `Windows_Release` | Latest stable Windows build — full README and source |
| `Linux_Release` | Linux build |
| `MacOS_Release` | macOS build |
| `TESTING-GENERAL` | Development and testing |

For installation instructions, the full tab reference, and the complete folder structure, see the **[Windows_Release branch README](https://github.com/Vider06/V0rtex/blob/Windows_Release/README.md)**.

---

## Quick Start

```
git clone -b Windows_Release https://github.com/Vider06/V0rtex.git
cd V0rtex
python v0rtex.py
```

On first launch V0RTEX opens the **Setup Wizard** automatically. It installs all dependencies, handles YARA, auto-detects tshark, builds the folder structure, and adds Defender exclusions.

**Requirements:** Windows 10/11 (64-bit) · Python 3.10+ · Internet connection for first-run setup

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

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full history.

---

## License

Copyright © 2024–2026 Vider_06. All rights reserved.  
See [LICENSE](LICENSE) for full terms.
