# **V0RTEX v1.1.1.X0**

**V0RTEX** (Vulnerability Oriented Recon Threat Exploitation eXaminer) is an advanced, high-performance malware analysis and SOC monitoring platform built entirely in Python \+ Tkinter.

Engineered for security researchers, incident responders, and SOC analysts, it combines local multi-engine intelligence with a self-updating, resilient bootloader architecture.

V \= Vulnerability · O \= Oriented · R \= Recon · T \= Threat · E \= Exploitation · X \= eXaminer

**Author:** Vider\_06

**Platform:** Windows 10 / 11 (64-bit) — Headless/CLI routine support for Unix environments

**Python:** 3.10 or higher — including 3.12, 3.13, 3.14

**License:** Copyright © 2024–2026 Vider\_06 — All rights reserved. See [LICENSE](https://github.com/Vider06/V0rtex/blob/main/LICENSE).

## **Index**

* [What is V0RTEX?](#bookmark=id.ub6zrvmfd9da)  
* [Features at a Glance](#bookmark=id.swxkgqe84jgu)  
* [Requirements](#bookmark=id.naifxpaizi2f)  
* [Installation](#bookmark=id.39g7tzar3w9f)  
  * [1\. Clone or download](#bookmark=id.6ss864a0dliw)  
  * [2\. Run](#bookmark=id.usdzkcfrmq7)  
  * [3\. Setup Wizard](#bookmark=id.w44qkvz45983)  
  * [4\. Configure API keys](#bookmark=id.gbkef2yfkeb5)  
  * [5\. Download YARA rules](#bookmark=id.dy7yacdnwhgm)  
* [Folder Structure](#bookmark=id.ubedegd41u22)  
* [Tab Reference](#bookmark=id.bq134398y0f3)  
  * [🏠 HOME](#bookmark=id.emr8hhh37dpr)  
  * [📋 LOGS](#bookmark=id.uxokt0zgejxi)  
  * [📊 CHRT — Charts](#bookmark=id.7qm6cmem6w49)  
  * [📁 REP — Reports](#bookmark=id.mi1pwvlbfdq)  
  * [🎯 IOC](#bookmark=id.dwh17omy2an5)  
  * [🛡 YARA](#bookmark=id.gm70o96yy8oy)  
  * [⚡ PERF](#bookmark=id.oghn2iw498pl)  
  * [⏱ TL — Timeline](#bookmark=id.9fz665p061zr)  
  * [🔬 SB — Sandbox](#bookmark=id.1yyeo2omsysr)  
  * [🧠 AI — Intelligence](#bookmark=id.5l6fex6t7qy)  
  * [🌐 NET — Network](#bookmark=id.kjc2urs8egs4)  
  * [🔒 PROT — App Protection](#bookmark=id.29ijn6ypcsft)  
  * [🔐 CRYPT — Cryptography](#bookmark=id.fzhu1eg6uw1c)  
  * [⚠ DZ — Danger Zone](#bookmark=id.m1odcc920eih)  
* [Supported APIs](#bookmark=id.5iso0yntferd)  
* [Security & Operational Resiliency](#bookmark=id.kbusowrrpiqf)  
* [Crash Recovery](#bookmark=id.29fabmryp38a)  
* [Advanced Update Architecture](#bookmark=id.mlv1x25sgom)  
* [Version Scheme](#bookmark=id.nt2ylvlgg8z)  
* [Contributing](#bookmark=id.s9uwxgthla6a)  
* [License](#bookmark=id.b4dq5tk554u7)

## **What is V0RTEX?**

V0RTEX is a comprehensive threat intelligence and malware triage ecosystem. It covers the full analysis pipeline: from localized static auditing (YARA, fuzzy hashing, cryptographic inspections, PE header decoding) and deep-learning contextual mapping, through dynamic monitoring (asynchronous network sniffing, Tor/Proxy routing, process auditing) to secure containment.

Built on a decoupled, modular framework, the core runtime executes hand-in-hand with an autonomous, self-updating infrastructure (v0rtex\_adapter.py) ensuring persistent operation, hardened anti-analysis protection, and automated disaster recovery rollbacks without leaving traces in the host system.

## **Features at a Glance**

| Area | Details |
| :---- | :---- |
| **AI Core** | Local AI Core Module · Semantic vulnerability mapping · Intelligent contextual threat analysis · Advanced local ML engine |
| **Guardian & Panic** | Anti-analysis & sandbox evasion detection · Active environment verification · State-corruption automated hooks · Forensic emergency lockdown |
| **Self-Destruct** | Volatile data wiping protocol · Counter-forensics deployment · Secure purge of keys, cached items, and Temp\_Log\_Storage |
| **YARA** | Custom rule editor · Community library downloader · String deobfuscator · Sigma rule viewer · yara-python / yara-x multi-engine compatibility shim |
| **VirusTotal** | File scan · Hash lookup · Bulk batch operations · Automated upload pipelines · Rescan scheduling |
| **PE Inspector** | Structural header analysis · Import/Export directory mapping · Suspicious API detection · Per-section entropy calculations · Import Hash (imphash) analyzer |
| **IOC Engine** | Automated regex extraction (IPs, domains, URLs, hashes, emails, CVEs, registry paths, Win32 APIs) · MITRE ATT\&CK technique mapping · Bulk reputation feeds · Secret scanner |
| **Sandbox** | Directory drop zone watcher · Dynamic runtime monitoring · Token extractors · Automated Cuckoo/CAPE framework integration |
| **Network** | PCAP capturing (tshark) · Port mapping · DNS/WHOIS/SSL certificate chain auditing · Ping · Outbound Proxy & Tor proxies · Noise generator · Live traffic monitor · Connection state graphs |
| **Crypto / Encoding** | AES-256-GCM · RSA · SHA-3 · BLAKE2 · Vigenère · Base64/Hex/XOR · JWT decoder · Hash structure inspector · ROT |
| **Threat APIs** | VirusTotal · MalwareBazaar · AbuseIPDB · URLScan.io · AlienVault OTX · Shodan · GreyNoise · HybridAnalysis |
| **Process Auditing** | Live tree inspection · Service trackers · Startup items · Active handles · Environment variables · Low-level registry browser |
| **Lookup Module** | Multi-vector lookups (Hex, Document macros, Signatures, Binary Patterns (BINPAT), Fuzzy hashes via rolling Jaccard scores) |
| **Privacy Layer** | Strict log censor module · Auto-censor configurations · Category-specific text filtering · Isolated log storage buffers |
| **System Check** | Windows Defender state auditing · SFC/DISM direct invocations · SMART hardware telemetry · Startup persistence scans · Multi-stage System Fixer |
| **Bootloader Engine** | Fully decoupled multi-hop Trampoline updates · Self-updating adapter · Structural folder builder · Emergency rollbacks |

**22 main tabs · 95+ sub-tabs**

## **Requirements**

* Windows 10 or 11 (64-bit)  
* Python 3.10 or higher  
* Internet connection (for automated dependency setups, threat feed syncs, and remote updates)  
* Elevated privileges (Administrator rights) — Highly recommended for low-level process hooking, network socket capturing, and system integrity commands.

## **Installation**

### **1\. Clone or download**

git clone \-b Windows\_Release \[https://github.com/Vider06/V0rtex.git\](https://github.com/Vider06/V0rtex.git)  
cd V0rtex

Or extract the latest deployment package directly from the [Releases](https://github.com/Vider06/V0rtex/releases) tab.

### **2\. Run**

python v0rtex.py

### **3\. Setup Wizard**

On a cold start, V0RTEX dynamically flags the missing environment state and deploys an interactive **Setup Wizard**:

* Resolves all Python dependencies via pip with sequential fallback routines.  
* Deploys the YARA multi-engine backend via a prioritized wheel \-\> yara-x \-\> source compilation pipeline.  
* Scans system paths for Wireshark/tshark binaries, mapping configuration arguments.  
* Instantiates structural filesystem architectures inside v0rtex\_utils/.  
* Provisions explicit Windows Defender exclusions over the workspace directory.

### **4\. Configure API keys**

Navigate to **CFG** → **API KEYS** to insert optional telemetry tokens (VirusTotal, Shodan, etc.). Keys persist strictly inside your local encrypted config.json.

### **5\. Download YARA rules**

Navigate to **YARA** → **LIBRARY** to batch-download community detection signatures (Neo23x0, Elastic, Avast).

## **Folder Structure**

All dynamic data and system logs have been strictly centralized under v0rtex\_utils/ to ensure a portably isolated application environment.

V0rtex\_System/  
├── V0RTEX\_v1.1.1.X0/                 ← Core installation directory  
│   ├── v0rtex.py                     \[setup\]   The primary application script  
│   ├── config.json                   \[setup\]   Encrypted configurations & API keys  
│   ├── config.json.bak               \[runtime\] Delta configuration backup state  
│   ├── scan\_history.db               \[setup\]   SQLite historical assessment cache  
│   ├── whitelist.txt                 \[setup\]   SHA-256 exclusion lists  
│   ├── notes.txt                     \[setup\]   Scratchpad database  
│   ├── requirements.txt              \[setup\]   Explicit dependency maps  
│   ├── launch.bat                    \[setup\]   Privilege launcher  
│   ├── \_setup\_complete               \[setup\]   Environmental environment sentinel  
│   ├── modules/                      \[setup\]   Internal analysis extensions  
│   ├── rules/                        \[startup\] Local compiled signature assets  
│   ├── reports/                      \[startup\] Asynchronous HTML/JSON assessment sheets  
│   ├── reports\_pdf/                  \[setup\]   Generated PDF reports  
│   ├── quarantine/                   \[startup\] Encrypted storage (.quar XOR-obfuscated)  
│   ├── backups/                      \[startup\] local state backup archives  
│   ├── sandbox\_env/                  \[setup\]   Containment folder  
│   │   └── drop/                     ← Automated sandbox ingestion entrypoint  
│   ├── threat\_feeds/                 \[setup\]   Imported IOC datasets  
│   └── pcap\_dumps/                   \[setup\]   Packet inspection dumps  
│  
├── v0rtex\_utils/                     ← Centralized utility utilities & system logs  
│   ├── .vx\_meta/  
│   │   └── vx\_version                \[setup\]   Dynamic metadata tracking matrix  
│   ├── \_v0rtex\_running.lock          \[runtime\] Mutex single-instance system lock  
│   ├── censor\_config.json            \[runtime\] Censor script filter definitions  
│   ├── v0rtex\_updater.py             \[setup\]   Secondary update proxy  
│   ├── v0rtex\_recovery\_ui.py         \[setup\]   Standalone recovery interface  
│   ├── v0rtex\_reinstall.py           \[setup\]   Full recovery tool  
│   ├── v0rtex\_uninstall.py           \[setup\]   Wipe script  
│   ├── v0rtex\_log\_censor.py          \[setup\]   Censor logic handler  
│   ├── Crash\_Full\_Report/            \[setup\]   Verbose debug structures  
│   ├── Temp\_Log\_Storage/             \[startup\] Censor queue buffer storage  
│   │   ├── session\_log/  
│   │   ├── admin\_log/  
│   │   ├── update\_log/  
│   │   └── recovery\_ops/  
│   ├── UNCENSORED/                   \[startup\] Raw pre-flush log mirrors  
│   └── debug\_log/                    \[startup\] Persistent telemetry directories  
│       ├── crash\_log/  
│       ├── session\_log/  
│       └── trampoline\_log/  
│  
└── V0rtex\_backups/                   ← Out-of-tree long-term safe storage

## **Tab Reference**

### **🏠 HOME**

* **📊 DASHBOARD** — Real-time scan statistics, ingestion threat indicators, and analytical quick actions.  
* **ℹ INFO** — Environmental data, driver checking, and interpreter diagnostics.  
* **README** — Fully integrated interactive copy of this manual.

### **📋 LOGS**

Divided interface showcasing a verbose **FILE OPERATIONS** ledger and a global **DEBUG LOG** tracing backend background worker threads.

### **📊 CHRT — Charts**

Renders mathematical metrics via custom **ENT** (entropy distribution scales) and **HEAT** (malicious activity vectors) visualization charts.

### **📁 REP — Reports**

Local report indexer with native file tree views and a built-in side-by-side hexadecimal/text delta comparator (**DIFF** engine).

### **🎯 IOC**

Tracks indicator sets natively. Features specialized sub-modules for pattern extraction (**EXTRACT**), **MITRE** ATT\&CK behavioral profiling, and deep **IMPHASH** clustering algorithms for grouping compiled malware families.

### **🛡 YARA**

Authoring and processing core. Includes a functional IDE with syntax verifiers (**RULE EDITOR**), a rule feed harvester (**LIBRARY**), and string deobfuscation helpers (**DEOBF**).

### **⚡ PERF**

Asynchronous performance tracking monitor mapping hardware cycles, disk overheads, and context switches down to individual process IDs.

### **🔬 SB — Sandbox**

A behavioral sandbox dashboard that interfaces directly with local virtualization hooks (**Cuckoo/CAPE**) and implements an active local file watcher over the automated execution drop zone.

### **🧠 AI — Intelligence**

The new intelligent operational core of V0RTEX. Leverages localized engines to construct relational graphs of extracted indicators, map semantic vulnerability vectors, and generate context-driven threat briefs.

### **🌐 NET — Network**

Advanced network orchestration hub. Includes tools for traffic inspections (tshark **PCAP** loops), automated **Tor** anonymous proxy chaining, outbound global **Proxy** configurations, background white-noise obfuscation engines (**Noise Gen**), and a scrolling timeline charting system connection allocations (**Conn Stats**).

### **🔒 PROT — App Protection**

Hardened defensive perimeter controller:

* **Guardian** — Continuous background integrity agent validating environment traits.  
* **Self-Defense** — Implements thread monitoring logic to block debug attachments or termination requests.  
* **Panic & Self-Destruct** — Triggers programmatic emergency states, executing counter-forensics data purges when unhandled environment compromises occur.  
* **System Check & Fixer** — Directly executes 6-step health inspections via Windows subsystem frameworks (SFC, DISM, MpComputerStatus), provisioning automated remediation blueprints on error detections.

## **Supported APIs**

All cloud modules function asynchronously via token injection. Local analytical engines remain independent.

| Provider | Purpose |
| :---- | :---- |
| **VirusTotal** | Global scanning, hash queries, bulk ingestion pipelines |
| **MalwareBazaar** | Sample pulling, automated threat signature checking |
| **AbuseIPDB** | Real-time IP address reputation auditing |
| **URLScan.io** | Remote URL behavior visualization |
| **AlienVault OTX** | Indicator of Compromise pulse matching |
| **Shodan & GreyNoise** | Port scans, botnet telemetry, scanner noise parsing |
| **HybridAnalysis** | Remote cloud sandbox executions |

## **Security & Operational Resiliency**

* **AV False-Positive Attenuation:** Critical runtime strings, high-privilege PowerShell execution structures, and core configuration signatures are never kept as literal primitives inside the codebase. They are reconstructed dynamically in memory or drawn through external meta matrices.  
* **Privilege Separation Rules:** If executed without elevated administrative rights, V0RTEX drops restricted features (e.g., direct kernel auditing, packet sniffing) gracefully while maintaining full analytical capability across user-space tools.

## **Crash Recovery**

If a severe runtime crash occurs, the global exception handling vectors instantly bypass application state lockouts, deploying a specialized **Recovery Terminal**:

* Generates descriptive execution stack mirrors inside v0rtex\_utils/debug\_log/crash\_log/.  
* Features an isolated UI file (v0rtex\_recovery\_ui.py) capable of running independently to perform file repairs, clean volatile caches, or perform granular version rollbacks.

## **Advanced Update Architecture**

V0RTEX utilizes a highly advanced, fully decoupled update pipeline driven by v0rtex\_adapter.py:

\[V0RTEX Core\] ──► Spawns Adapter ──► \[V0RTEX Terminated\]  
                                            │  
   ┌────────────────────────────────────────┘  
   ▼  
\[Adapter Self-Update\] ──► Checks version. Manifest match?  
                                            │  
   ┌────────────────────────────────────────┘  
   ▼  
\[Trampoline Loop\] ──► Gap \> 5? Fetches intermediate versions sequentially  
                                            │  
   ┌────────────────────────────────────────┘  
   ▼  
\[6-Step Pipeline\] ──► Kill ──► Deps ──► Pip ──► Dirs ──► Meta ──► Launch  
                                                                    │  
   ┌────────────────────────────────────────────────────────────────┘  
   ▼  
\[Boot Success?\] ───► YES ──► Safe exit & self-destruct script (.del)  
                └───► NO  ──► Emergency Restore zip deployment

This ensures that even if a user updates from an extremely old legacy version, the system self-remedies by hopping through required dependency baselines safely.

## **Version Scheme**

MAJOR . FEATURE\_RELEASE . MAINTENANCE . BUGFIX

Example: 1.1.1.X0  
  1   \= Major architectural state  
  1   \= Feature update release (AI integration)  
  1   \= Small baseline enhancement  
  X0  \= Initial release patch version

## **Contributing**

Analytical contributions are welcome. Please submit detailed issue reports containing:

* V0RTEX Version metadata string.  
* Local interpreter information (python \--version).  
* Verbose crash output log pulled from v0rtex\_utils/debug\_log/crash\_log/.

## **License**

Copyright © 2024–2026 Vider\_06. All rights reserved.

Distributed under custom restrictive software terms. See the enclosed LICENSE document for specific details.

eof  
