# OPL-ZSO-Converter-Termux

Convert PlayStation 2 ISO files to ZSO format directly on Android using Termux and Open PS2 Loader's ziso.py.

## Features

* Batch conversion of ISO files to ZSO.
* Automatically creates the output directory.
* Moves converted ZSO files to the destination folder.
* Deletes original ISO files after successful conversion.
* Skips files that have already been converted.
* Simple and lightweight.

## Requirements

* Android device
* Termux
* Python 3
* Git
* LZ4 Python library

## Installation

Update Termux:
```bash
pkg update -y
pkg upgrade -y
```

Clone this repository and navigate into it:
```bash
git clone https://github.com/ClotiusB/OPL-ZSO-Converter-Termux.git
cd OPL-ZSO-Converter-Termux
```

Install required packages:
```bash
pkg install python git -y
```

Install the LZ4 dependency:
```bash
pip install lz4
```

Clone Open PS2 Loader (required for `ziso.py`):
```bash
git clone https://github.com/ps2homebrew/Open-PS2-Loader.git
```
## Directory Structure

Place your ISO files in:
* `/sdcard/Download/Iso`

Converted files will be saved to:
* `/sdcard/Download/Zso`

### Example:
```text
Download/
├── Iso/
│   ├── God of War.iso
│   ├── Gran Turismo 4.iso
│   └── Shadow of the Colossus.iso
│
└── Zso/
```

## Configuration

You can also adjust the compression level:
```python
COMP_LEVEL = "2"
```

### Compression levels:

| Level | Description |
| :--- | :--- |
| **0** | No compression |
| **1-12** | Increasing compression ratio |

## Usage

Run the script:
```bash
python compress_isos.py
```

### What Happens
For every ISO file found:
1. The ISO is compressed into ZSO format.
2. The generated file is verified.
3. The ZSO file is moved to `/sdcard/Download/Zso`.
4. The original ISO is deleted.
5. The next ISO is processed.

### Example Output
```text
[1/3] Processing: God of War.iso
[OK] Moved to: /sdcard/Download/Zso/God of War.zso
[OK] Deleted source ISO: God of War.iso

[2/3] Processing: Gran Turismo 4.iso
[OK] Moved to: /sdcard/Download/Zso/Gran Turismo 4.zso
[OK] Deleted source ISO: Gran Turismo 4.iso

===== SUMMARY =====
ISO files found : 3
Converted       : 3
Failed/Skipped  : 0
```

## Warning

> ⚠️ **Original ISO files are permanently deleted after successful conversion.**
> 
> Make sure your ZSO files are working correctly before removing any backups.

## Compatibility

* Open PS2 Loader (OPL) 1.2.0+
* Android (Termux)
* Python 3

## License

[MIT License](https://en.wikipedia.org/wiki/MIT_License)
