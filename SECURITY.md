# Security Policy — V0RTEX

## ⚠️ Nature of this project

V0RTEX is a **malware analysis platform**. By design it opens, parses, decompiles and executes code from untrusted files. It also spawns subprocesses with elevated privileges, captures network traffic, and interacts directly with the Windows kernel through PowerShell, WMI, and ctypes.

**Do not run V0RTEX on a production machine or on any system that holds sensitive data you cannot afford to lose.** Use a dedicated analysis VM or an isolated lab environment.

---

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.9.9.X (current) | ✅ Yes |
| 0.9.8.X | ⚠️ Best-effort — upgrade recommended |
| < 0.9.8 | ❌ No |

---

## Reporting a vulnerability

If you find a security issue in V0RTEX itself (not in a file you are analyzing with it), please **do not open a public GitHub issue**.

Report privately via one of these channels:

- **GitHub private security advisory** — [Security → Report a vulnerability](https://github.com/Vider06/V0rtex/security/advisories/new)
- **GitHub Discussions** — open a private thread tagged `security`

Include:

- V0RTEX version (shown in the bottom status bar or `version.txt`)
- Python version and Windows version
- A clear description of the issue and how to reproduce it
- Whether it requires admin rights to exploit
- The relevant section of `debug_log/` if applicable

I will respond within **7 days** and aim to release a patch within **30 days** for confirmed critical issues.

---

## Known security considerations

These are by design, not bugs:

### Admin privileges
V0RTEX requests admin rights on first launch and during setup. This is required for:
- Windows Defender exclusion management
- `sfc /scannow` and `dism /RestoreHealth`
- Raw network capture via tshark
- Process tree inspection and termination
- Registry access

The UAC prompt is triggered via `ShellExecute` with `runas`. After setup, the main UI runs at **user integrity level** — the admin trampoline exits immediately after launching the user-level process.

### Subprocess execution
V0RTEX spawns subprocesses for tshark, PowerShell, SFC, DISM, and pip. All subprocess calls use explicit argument lists (no `shell=True` for user-supplied paths). PowerShell commands are assembled from fragments at runtime to reduce static AV false positives — this is intentional, not obfuscation.

### API keys
API keys (VirusTotal, Shodan, AbuseIPDB, etc.) are stored in plain text in `config.json` inside the install directory. They are never transmitted anywhere other than their respective official API endpoints. Do not commit `config.json` to a public repository.

### Network traffic
V0RTEX sends data externally only when you explicitly trigger a lookup (VirusTotal scan, IP reputation, WHOIS, etc.). There is no telemetry, no analytics, no automatic file upload. The auto-update check (`CFG → UPDATER`) only fetches `version.txt` and `update_manifest.json` from this repository — no executable code is fetched without your explicit confirmation.

### Analyzed files
V0RTEX does **not** sandbox the files it analyzes. Static analysis (hashes, PE headers, strings, entropy, YARA) is safe. If you use the **Sandbox tab** or the **Cuckoo/CAPE integration** to actually execute malware, that execution happens on your machine or your configured sandbox instance — not inside V0RTEX.

---

## AV false positives

Windows Defender and other AV engines may flag V0RTEX due to:

- YARA rule strings that match malware patterns
- PowerShell command fragments assembled at runtime
- `ctypes` calls to low-level Windows APIs
- The presence of PE parsing and entropy analysis code

The setup wizard automatically adds the install folder to your Defender exclusion list. If Defender flags the file after download, add `v0rtex.py` manually before running it.

If you need to verify the file integrity, SHA-256 hashes for each release are published in the [Releases](https://github.com/Vider06/V0rtex/releases) page.

---

## Responsible use

V0RTEX is a research and analysis tool. Do not use it to analyze files you do not have permission to inspect, or to access systems you do not own. The author is not responsible for misuse.

---

*Copyright © 2024–2026 Vider\_06 — All rights reserved.*
