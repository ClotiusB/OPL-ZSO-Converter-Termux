#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path

ISO_DIR = Path("/sdcard/Download/Iso")
ZSO_DIR = Path("/sdcard/Download/Zso")

# Path to ziso.py
ZISO = "/data/data/com.termux/files/home/Open-PS2-Loader/pc/ziso.py"

# Compression level (0-12)
COMP_LEVEL = "2"


def main():
    ZSO_DIR.mkdir(parents=True, exist_ok=True)

    if not ISO_DIR.exists():
        print(f"[ERROR] Directory not found: {ISO_DIR}")
        return

    iso_files = sorted(ISO_DIR.glob("*.iso"))

    if not iso_files:
        print("[INFO] No ISO files found.")
        return

    total_files = len(iso_files)
    converted_files = 0

    for index, iso_file in enumerate(iso_files, start=1):
        game_name = iso_file.stem

        temp_zso = ISO_DIR / f"{game_name}.zso"
        final_zso = ZSO_DIR / f"{game_name}.zso"

        print(f"\n[{index}/{total_files}] Processing: {iso_file.name}")

        if final_zso.exists():
            print("[SKIP] ZSO file already exists in destination.")
            continue

        command = [
            "python",
            ZISO,
            "-c",
            COMP_LEVEL,
            str(iso_file),
            str(temp_zso)
        ]

        try:
            result = subprocess.run(command)

            if result.returncode != 0:
                print("[ERROR] Compression failed.")
                continue

            if not temp_zso.exists() or temp_zso.stat().st_size == 0:
                print("[ERROR] Invalid ZSO file generated.")
                continue

            shutil.move(str(temp_zso), str(final_zso))
            print(f"[OK] Moved to: {final_zso}")

            iso_file.unlink()
            print(f"[OK] Deleted source ISO: {iso_file.name}")

            converted_files += 1

        except Exception as error:
            print(f"[ERROR] {error}")

    print("\n===== SUMMARY =====")
    print(f"ISO files found : {total_files}")
    print(f"Converted       : {converted_files}")
    print(f"Failed/Skipped  : {total_files - converted_files}")


if __name__ == "__main__":
    main()
