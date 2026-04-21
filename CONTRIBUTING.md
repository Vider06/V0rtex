# Contributing to V0RTEX

## License and Ownership

V0RTEX is proprietary software. Copyright © 2024–2026 Vider_06. All rights reserved.

By submitting a contribution (Pull Request, patch, or any code change), you grant the Author (Vider_06) a perpetual, worldwide, irrevocable, royalty-free license to use, modify, integrate, and distribute your contribution as part of V0RTEX.

You acknowledge that:
- Your contribution may be modified or merged without further notice
- Your contribution becomes part of V0RTEX and is subject to its license terms
- You retain authorship of your original submission, but not exclusive rights once merged

You agree that:
- You will not assert any ownership claims over merged contributions within V0RTEX
- You are the sole author of the submitted code
- You have the legal right to grant the above license
- Your contribution does not include malicious, hidden, or unauthorized functionality

If you do not agree, you must not submit a contribution.

---

## Before You Start

V0RTEX is a **single-file project** (`v0rtex.py`). All contributions must fit within this constraint — no new top-level files or external launchers unless specifically discussed with the maintainer first.

Please read through the existing code style and tab structure in `v0rtex.py` before writing anything new.

---

## How to Contribute

### Reporting Bugs

Open an issue and include:

- V0RTEX version (shown in the bottom status bar)
- Python version (`python --version`)
- Windows version (10 or 11, 64-bit)
- The relevant crash report from `V0rtex_System/.../debug_log/`
- Steps to reproduce the issue

### Suggesting Features

Open an issue with the label `enhancement`. Describe:

- What the feature does
- Which tab or workflow it belongs to
- Why it's useful for malware analysis

### Submitting a Pull Request

1. **Fork** the repository and create a branch from `main`
2. Make your changes in `v0rtex.py` only (unless agreed otherwise)
3. Do **not** add Python `#` comments — V0RTEX intentionally avoids inline comments
4. Test your changes on Windows 10 or 11 with Python 3.10+
5. Update `CHANGELOG.md` with a short description of your change
6. Open a PR against `main` with a clear title and description

### YARA Rules / Detection Logic

If you're contributing detection rules or IOC extraction patterns, include at least one test case demonstrating the rule fires correctly.

---

## What Not to Do

- Do not submit live malware samples or weaponized payloads in any form
- Do not open PRs that add external dependencies without prior discussion
- Do not modify `version.txt` or `update_manifest.json` — those are managed by the maintainer
- Do not submit code copied or adapted from other projects without prior explicit written permission from the Author

---

## Code Style

- Python 3.10+ compatible
- Tkinter for all UI — no third-party UI frameworks
- No inline `#` comments in touched code
- Keep new functionality self-contained within its relevant tab/class

---

## Questions

Open a [Discussion](https://github.com/Vider06/V0rtex/discussions) for anything that doesn't fit neatly into an issue.  
For permissions beyond personal use, contact the Author directly: [@Vider06](https://github.com/Vider06)
