"""Build GRC Agent local client exe and package as zip."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORTABLE_DIR = ROOT / "GRC-Agent-Portable"
ZIP_PATH = ROOT / "GRC-Agent-Portable.zip"


def step(msg):
    print(f"\n{'='*50}")
    print(f"  {msg}")
    print(f"{'='*50}\n", flush=True)


def run(cmd, cwd=ROOT):
    result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-2000:] if result.stderr else "(no stderr)")
        sys.exit(1)
    return result.stdout


def main():
    # 1. Build exe
    step("1/4  Building GRCAgent.exe with PyInstaller...")
    if not (ROOT / "GRCAgent.spec").exists():
        print("ERROR: GRCAgent.spec not found")
        sys.exit(1)
    run("python -m PyInstaller GRCAgent.spec --noconfirm")
    exe_path = ROOT / "dist" / "GRCAgent.exe"
    if not exe_path.exists():
        print("ERROR: Build failed - GRCAgent.exe not found")
        sys.exit(1)
    size_mb = exe_path.stat().st_size / 1024 / 1024
    print(f"OK: GRCAgent.exe ({size_mb:.1f} MB)")

    # 2. Prepare portable folder
    step("2/4  Preparing GRC-Agent-Portable/ folder...")
    if PORTABLE_DIR.exists():
        shutil.rmtree(PORTABLE_DIR)
    PORTABLE_DIR.mkdir(parents=True)
    (PORTABLE_DIR / "runtime" / "reports").mkdir(parents=True)

    # Copy exe
    shutil.copy2(exe_path, PORTABLE_DIR / "GRCAgent.exe")

    # Copy .env (Turso credentials)
    env_src = ROOT / ".env"
    if env_src.exists():
        shutil.copy2(env_src, PORTABLE_DIR / ".env")
        print("OK: .env (Turso credentials)")
    else:
        print("WARNING: .env not found - users will need to create it")

    # Copy contacts.json
    contacts_src = ROOT / "contacts.json"
    if contacts_src.exists():
        shutil.copy2(contacts_src, PORTABLE_DIR / "contacts.json")
        print("OK: contacts.json")

    # Create launcher bat
    (PORTABLE_DIR / "启动.bat").write_text(
        '@echo off\ncd /d "%~dp0"\nstart "" "GRCAgent.exe"\n',
        encoding="utf-8",
    )

    # Create README
    (PORTABLE_DIR / "README.txt").write_text(
        "GRC Agent - Local Client\n"
        "========================\n\n"
        "Quick Start:\n"
        "1. Double-click 启动.bat or GRCAgent.exe\n"
        "2. Login with your GRC Agent account\n"
        "3. All data is shared with the web version\n\n"
        "Requirements:\n"
        "- Windows 10/11 (64-bit)\n"
        "- Outlook desktop app installed\n"
        "- VW internal network access\n",
        encoding="utf-8",
    )

    print(f"OK: Portable folder ready at {PORTABLE_DIR}")

    # 3. Create zip
    step("3/4  Creating GRC-Agent-Portable.zip...")
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    shutil.make_archive(
        str(PORTABLE_DIR),  # base name (without .zip)
        "zip",
        root_dir=str(PORTABLE_DIR),
    )
    zip_mb = ZIP_PATH.stat().st_size / 1024 / 1024
    print(f"OK: {ZIP_PATH} ({zip_mb:.1f} MB)")

    # 4. Done
    step("4/4  Build complete!")
    print(f"  exe:  {PORTABLE_DIR / 'GRCAgent.exe'} ({size_mb:.1f} MB)")
    print(f"  zip:  {ZIP_PATH} ({zip_mb:.1f} MB)")
    print(f"\n  Distribute the zip to users.")
    print(f"  Users unzip and double-click 启动.bat to run.")


if __name__ == "__main__":
    main()
