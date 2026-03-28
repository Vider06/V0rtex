"""
V0RTEX — Clean Test Environment
Rimuove tutti i pacchetti V0RTEX e VS Build Tools per testare il setup da zero.
"""
import subprocess, sys, os, shutil

PACKAGES = [
    "requests", "pefile", "matplotlib", "tkinterdnd2", "psutil",
    "fpdf2", "watchdog", "pystray", "Pillow", "cryptography",
    "reportlab", "yara-python",
]

print("=" * 60)
print("  V0RTEX — Clean Test Environment")
print("=" * 60)

# ── 1. Disinstalla pacchetti pip ──────────────────────────────
print("\n[ 1 / 2 ]  Rimozione pacchetti pip...\n")
for pkg in PACKAGES:
    r = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", pkg],
        capture_output=True, text=True
    )
    if "Successfully uninstalled" in r.stdout:
        print(f"  ✓ {pkg}")
    elif "not installed" in r.stdout or "not installed" in r.stderr:
        print(f"  · {pkg}  (non era installato)")
    else:
        print(f"  ~ {pkg}  ({(r.stderr or r.stdout).strip()[:60]})")

# ── 2. Rimuovi pip stesso (simula pythoncore minimale) ────────
print("\n[ 2 / 2 ]  Rimozione pip...\n")
r2 = subprocess.run(
    [sys.executable, "-m", "pip", "uninstall", "-y", "pip"],
    capture_output=True, text=True
)
if r2.returncode == 0:
    print("  ✓ pip rimosso")
else:
    print(f"  ~ {r2.stderr.strip()[:80]}")

# ── 3. VS Build Tools (winget) ────────────────────────────────
print("\n[ + ]  VS Build Tools\n")
if sys.platform == "win32" and shutil.which("winget"):
    inp2 = input("  Vuoi rimuovere VS Build Tools 2022 via winget? [s/N] ").strip().lower()
    if inp2 == "s":
        print("  → winget uninstall Microsoft.VisualStudio.2022.BuildTools ...")
        r3 = subprocess.run(
            ["winget", "uninstall", "--id",
             "Microsoft.VisualStudio.2022.BuildTools", "--silent"],
            capture_output=True, text=True, timeout=300
        )
        if r3.returncode == 0:
            print("  ✓ VS Build Tools rimossi")
        else:
            print(f"  ~ exit {r3.returncode}: {(r3.stderr or r3.stdout).strip()[:120]}")
    else:
        print("  · VS Build Tools mantenuti")
else:
    print("  · winget non disponibile o non Windows — salta")

print("\n" + "=" * 60)
print("  Fatto. Ora puoi rieseguire v0rtex.py per testare il setup.")
print("=" * 60)
