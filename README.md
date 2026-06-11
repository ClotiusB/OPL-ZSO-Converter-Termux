# OPL-ZSO-Converter-Termux

Convert PlayStation 2 ISO files to ZSO format directly on Android using Termux and Open PS2 Loader's ziso.py.

## Features

* Batch conversion of ISO files to ZSO.
* Automatically creates the output directory.
* Moves converted ZSO files to the destination folder.
* **Choose whether to keep or delete original ISO files** after successful conversion.
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

### Install Git

Install Git package:
```bash
pkg install git -y
```

Verify Git installation:
```bash
git --version
```

### Initial Termux Configuration

Grant Termux access to internal storage:
```bash
termux-setup-storage
```
This will prompt you to allow Termux access to your device's internal storage. You must accept this to access `/sdcard/Download`.

Install Python 3 and pip:
```bash
pkg install python python-pip -y
```

### Clone Open PS2 Loader (required for ziso.py)

Clone Open PS2 Loader first:
```bash
git clone https://github.com/ps2homebrew/Open-PS2-Loader.git
```

### Clone and Setup Repository

Clone this repository and navigate into it:
```bash
git clone https://github.com/ClotiusB/OPL-ZSO-Converter-Termux.git
cd OPL-ZSO-Converter-Termux
```

Install the LZ4 dependency:
```bash
pip install lz4
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

The script will ask you two things:

1. **Language Selection**: Choose between Portuguese (Brazil) or English (American)
2. **ISO Handling Preference**: 
   - Keep ISO files after compression
   - Remove ISO files after compression

After making your choices, for every ISO file found:
1. The ISO is compressed into ZSO format.
2. The generated file is verified.
3. The ZSO file is moved to `/sdcard/Download/Zso`.
4. Based on your preference, the original ISO is either kept or deleted.
5. The next ISO is processed.

### Example Output
```text
[1/3] Processing: God of War.iso
[OK] File moved successfully.
[OK] ISO kept

[2/3] Processing: Gran Turismo 4.iso
[OK] File moved successfully.
[OK] ISO deleted

===== SUMMARY =====
ISO files found : 3
Successfully converted : 3
Failed/Skipped  : 0
ISO files: Kept
```

## Notes

> ℹ️ **You control what happens to your ISO files.**
> 
> Before starting compression, choose whether to keep or delete your ISO files. This preference will be applied to all files in the batch.

## Compatibility

* Open PS2 Loader (OPL) 1.2.0+
* Android (Termux)
* Python 3

## License

[MIT License](https://en.wikipedia.org/wiki/MIT_License)
