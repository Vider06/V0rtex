# Security Policy — V0RTEX

## ⚠️ What this software does

V0RTEX is a **malware analysis and system security platform** for Windows. It is designed to open, parse, decompile, and inspect untrusted files using static analysis techniques. It also manages system-level operations including network capture, process control, registry access, and privilege escalation.

**V0RTEX is a power tool. It is not a toy and it is not a passive scanner.**
Use it on a dedicated analysis machine, a VM, or an isolated lab environment.
Do not run it on a production system or on any machine containing data you cannot afford to lose or expose.

---

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.9.9.X (current) | ✅ Active development, all fixes applied here |
| 0.9.8.X | ⚠️ Best-effort — upgrade strongly recommended |
| < 0.9.8 | ❌ No support |

---

## Architecture overview

V0RTEX is a **single-file Python application** (~33,000 lines) that runs entirely on the user's machine. There is no server-side component, no cloud backend, and no telemetry of any kind. All processing happens locally except for explicit user-triggered external lookups (VirusTotal, Shodan, AbuseIPDB, etc.).

The application consists of:
- A **setup wizard** that installs dependencies, creates the directory structure, writes embedded helper scripts, and configures Windows Defender exclusions
- A **main UI** built in Tkinter, running at user integrity level
- A set of **embedded helper scripts** written to disk at install time: `v0rtex_reinstall.py`, `v0rtex_uninstall.py`, `v0rtex_updater.py`, `v0rtex_recovery_ui.py`, `v0rtex_log_censor.py`
- A **trampoline mechanism** for privilege escalation (see below)

---

## Privilege model

V0RTEX operates at **two distinct privilege levels**:

### User level (normal operation)
The main application window runs at standard user integrity level. Most features (file scanning, YARA, VirusTotal, PE analysis, entropy, hex viewer, network monitor, etc.) do not require elevation.

### Admin level (specific operations)
The following operations require administrator privileges and will prompt for UAC:
- Windows Defender exclusion management (`Add-MpPreference`)
- System File Checker (`sfc /scannow`) and DISM (`dism /RestoreHealth`)
- Raw network packet capture via tshark
- Controlled Folder Access (CFA) bypass for whitelisting
- Some registry read operations and process tree inspection
- Reinstall / Uninstall (these rewrite the install directory)

### Trampoline mechanism
When admin access is needed, V0RTEX does **not** restart itself as admin for normal operation. Instead, it uses a **trampoline pattern**:
1. A small stdlib-only Python script is written to the system TEMP folder
2. The script is launched via `ShellExecute` with the `runas` verb (triggers UAC)
3. The trampoline performs the privileged operation, then launches the main app at user level and self-deletes
4. The admin process exits immediately — it does not persist

This means the main V0RTEX window you use every day runs at user level, not admin level.

---

## Network and external communications

V0RTEX communicates externally **only when you explicitly trigger a lookup**. There is no background telemetry, no analytics, no automatic file upload.

External calls are made only to:
- **VirusTotal** — when you click "Scan" on a file or URL (requires API key)
- **Shodan** — IP/host lookup (requires API key)
- **AbuseIPDB** — IP reputation check (requires API key)
- **URLScan.io** — URL submission (requires API key)
- **MalwareBazaar** — hash lookup (optional key)
- **OTX (AlienVault)** — threat intelligence (optional key)
- **Greynoise** — IP context (optional key)
- **GitHub** — version check (`version.txt`) and update manifest (`update_manifest.json`) when you open the Updater tab
- **wireshark.org** — version check when the setup wizard verifies tshark
- **torproject.org** — only if you use the Tor install button

No executable code is fetched from GitHub without your explicit confirmation of an update. The update flow fetches the new `v0rtex.py` source, shows you the changelog, and requires a manual click to proceed.

---

## API keys and secrets

API keys are stored in plain text in `config.json` inside the install directory. They are:
- Never transmitted anywhere other than the respective official API endpoints they are associated with
- Never logged to any log file
- Automatically censored from log files if the "Auto-censor logs" option is enabled in setup or Settings → Privacy

**Do not commit `config.json` to a public repository.**

---

## Log files and privacy

V0RTEX writes several log files to `v0rtex_utils/debug_log/`:

- `session_log/` — session activity log (startup, checkpoints, settings changes, scan events)
- `silent_log/` — low-level boot log written before the UI starts (useful for diagnosing silent crashes)
- `crash_log/` — written when an unhandled exception occurs
- `trampoline_log/` — admin/elevation events
- `admin_log/` — UAC and privilege events
- `update_log/` — updater activity
- `setup_log/` — installation log
- `install_*.txt` — full installation transcript

**These logs may contain sensitive information** including file paths (which expose your Windows username), IP addresses, hostnames, and scanned file names.

### Auto-censor feature
If "Auto-censor logs" is enabled (checkbox in the setup wizard, or Settings → Privacy), all log writes are processed through a censor filter that redacts:
- IPv4 and IPv6 addresses
- Usernames embedded in file paths (`Users\<name>`)
- Email addresses
- MAC addresses
- Hostnames

When censoring is active:
- The log files in their normal locations contain censored content
- The original uncensored logs are saved separately in `debug_log/UNCENSORED/`

The `v0rtex_log_censor.py` utility (in `v0rtex_utils/`) can also be run standalone to batch-censor existing log files before sharing them.

---

## Subprocess execution

V0RTEX spawns external subprocesses for:
- `tshark` — network packet capture (launched with `CREATE_NO_WINDOW` on Windows)
- `python.exe` / `pip` — package management during setup and updates
- PowerShell — Windows Defender configuration, Zone.Identifier removal
- `sfc`, `dism` — system integrity checks (admin only)
- `winget` — optional installation of Wireshark and Tor Browser

All subprocess calls use explicit argument lists. `shell=True` is never used for paths or commands derived from user input. PowerShell commands are assembled from string fragments at runtime — this is intentional to reduce static AV false positives and is not obfuscation.

---

## Analyzed files

V0RTEX does **not** execute the files it analyzes during static analysis. The following operations are read-only and safe:
- SHA-256 / MD5 / SHA-1 hashing
- PE header parsing (pefile)
- Entropy calculation
- String extraction
- YARA rule matching
- Hex viewer
- IOC extraction (IPs, URLs, domains, registry keys)
- MITRE ATT&CK mapping

The following operations interact with external systems and involve user data leaving the machine:
- VirusTotal submission / hash lookup
- AbuseIPDB / Shodan / OTX / URLScan lookups

The **Sandbox tab** and **Cuckoo/CAPE integration** can execute files. When used, execution happens on your machine (local sandbox) or on your configured Cuckoo/CAPE instance — not inside V0RTEX itself. The Author is not responsible for damage caused by executing malware through the sandbox feature.

---

## AV false positives

Windows Defender and other AV engines may flag V0RTEX or flag it during operation due to:
- YARA rule strings that match malware patterns
- PowerShell command fragments assembled at runtime
- `ctypes` calls to low-level Windows APIs (`VirtualAlloc`, `NtQueryInformationProcess`, etc.)
- PE parsing and entropy analysis code
- The presence of quarantine and process-termination capabilities

The setup wizard automatically adds the install folder to your Defender exclusion list. If Defender flags `v0rtex.py` after download, add it manually before running.

SHA-256 hashes for each release are published on the [Releases](https://github.com/Vider06/V0rtex/releases) page. Verify the hash before running if you have any doubt about file integrity.

---

## Reporting a vulnerability

If you find a security issue in V0RTEX itself (not in a file you are analyzing with it), please **do not open a public GitHub issue**.

Report privately via:
- **GitHub private security advisory** — [Security → Report a vulnerability](https://github.com/Vider06/V0rtex/security/advisories/new)

Include:
- V0RTEX version (shown in the title bar or `v0rtex_utils/.vx_meta/vx_version`)
- Python version and Windows build
- A clear description of the issue and reproduction steps
- Whether it requires admin rights to exploit
- Relevant log excerpts from `debug_log/` if applicable

Response target: **7 days**. Patch target for confirmed critical issues: **30 days**.

---

## Responsible use

V0RTEX is a research and analysis tool intended for use on files and systems you own or have explicit permission to analyze. Do not use it to inspect files you are not authorized to access, or to perform operations on systems you do not control. The Author is not responsible for misuse.

---

*Copyright © 2024–2026 Vider\_06 — All rights reserved.*
