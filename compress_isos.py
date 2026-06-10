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

# Language setting (will be set by user)
LANGUAGE = None

# Translation dictionary
TRANSLATIONS = {
    "pt_BR": {
        "language_menu_title": "===== SELEÇÃO DE IDIOMA =====",
        "language_option_1": "1. Português Brasileiro",
        "language_option_2": "2. English (American)",
        "language_separator": "============================",
        "language_select": "Selecione uma opção (1 ou 2): ",
        "language_invalid": "[ERRO] Opção inválida. Digite 1 ou 2.",
        
        "iso_handling_title": "===== PREFERÊNCIA DE ISO =====",
        "iso_option_1": "1. Manter arquivos ISO após compressão",
        "iso_option_2": "2. Remover arquivos ISO após compressão",
        "iso_separator": "==============================",
        "iso_select": "Selecione uma opção (1 ou 2): ",
        "iso_invalid": "[ERRO] Opção inválida. Digite 1 ou 2.",
        
        "dir_not_found": "[ERRO] Diretório não encontrado: {path}",
        "no_iso_files": "[INFO] Nenhum arquivo ISO encontrado.",
        "processing": "[{index}/{total}] Processando: {filename}",
        "skip_exists": "[PULAR] Arquivo ZSO já existe no destino.",
        "error_compression": "[ERRO] Falha na compressão.",
        "error_invalid_zso": "[ERRO] Arquivo ZSO inválido gerado.",
        "ok_moved": "[OK] Movido para: {path}",
        "ok_kept": "[OK] ISO de origem mantida: {filename}",
        "ok_deleted": "[OK] ISO de origem deletada: {filename}",
        "error_exception": "[ERRO] {error}",
        
        "summary_title": "===== RESUMO =====",
        "summary_found": "Arquivos ISO encontrados: {total}",
        "summary_converted": "Convertidos: {converted}",
        "summary_failed": "Falhados/Pulados: {failed}",
        "summary_iso_status": "Arquivos ISO: {status}",
        "iso_kept": "Mantidos",
        "iso_removed": "Removidos",
    },
    "en_US": {
        "language_menu_title": "===== LANGUAGE SELECTION =====",
        "language_option_1": "1. Português Brasileiro",
        "language_option_2": "2. English (American)",
        "language_separator": "=============================",
        "language_select": "Select an option (1 or 2): ",
        "language_invalid": "[ERROR] Invalid choice. Please enter 1 or 2.",
        
        "iso_handling_title": "===== ISO HANDLING PREFERENCE =====",
        "iso_option_1": "1. Keep ISO files after compression",
        "iso_option_2": "2. Remove ISO files after compression",
        "iso_separator": "====================================",
        "iso_select": "Select an option (1 or 2): ",
        "iso_invalid": "[ERROR] Invalid choice. Please enter 1 or 2.",
        
        "dir_not_found": "[ERROR] Directory not found: {path}",
        "no_iso_files": "[INFO] No ISO files found.",
        "processing": "[{index}/{total}] Processing: {filename}",
        "skip_exists": "[SKIP] ZSO file already exists in destination.",
        "error_compression": "[ERROR] Compression failed.",
        "error_invalid_zso": "[ERROR] Invalid ZSO file generated.",
        "ok_moved": "[OK] Moved to: {path}",
        "ok_kept": "[OK] Kept source ISO: {filename}",
        "ok_deleted": "[OK] Deleted source ISO: {filename}",
        "error_exception": "[ERROR] {error}",
        
        "summary_title": "===== SUMMARY =====",
        "summary_found": "ISO files found: {total}",
        "summary_converted": "Converted: {converted}",
        "summary_failed": "Failed/Skipped: {failed}",
        "summary_iso_status": "ISO files: {status}",
        "iso_kept": "Kept",
        "iso_removed": "Removed",
    }
}


def get_language():
    """Ask user to choose between Portuguese (Brazil) and English (American)."""
    while True:
        print(TRANSLATIONS["pt_BR"]["language_menu_title"])
        print(TRANSLATIONS["pt_BR"]["language_option_1"])
        print(TRANSLATIONS["pt_BR"]["language_option_2"])
        print(TRANSLATIONS["pt_BR"]["language_separator"])
        
        choice = input(TRANSLATIONS["pt_BR"]["language_select"]).strip()
        
        if choice == "1":
            return "pt_BR"
        elif choice == "2":
            return "en_US"
        else:
            print(TRANSLATIONS["pt_BR"]["language_invalid"])


def t(key, **kwargs):
    """Get translated string for the current language."""
    text = TRANSLATIONS[LANGUAGE][key]
    if kwargs:
        return text.format(**kwargs)
    return text


def get_user_preference():
    """Ask user if they want to keep or remove ISO files after compression."""
    while True:
        print(f"\n{t('iso_handling_title')}")
        print(t("iso_option_1"))
        print(t("iso_option_2"))
        print(t("iso_separator"))
        
        choice = input(t("iso_select")).strip()
        
        if choice == "1":
            return True  # Keep ISO files
        elif choice == "2":
            return False  # Remove ISO files
        else:
            print(t("iso_invalid"))


def main():
    global LANGUAGE
    LANGUAGE = get_language()
    
    ZSO_DIR.mkdir(parents=True, exist_ok=True)

    if not ISO_DIR.exists():
        print(t("dir_not_found", path=ISO_DIR))
        return

    iso_files = sorted(ISO_DIR.glob("*.iso"))

    if not iso_files:
        print(t("no_iso_files"))
        return

    keep_isos = get_user_preference()

    total_files = len(iso_files)
    converted_files = 0

    for index, iso_file in enumerate(iso_files, start=1):
        game_name = iso_file.stem

        temp_zso = ISO_DIR / f"{game_name}.zso"
        final_zso = ZSO_DIR / f"{game_name}.zso"

        print(t("processing", index=index, total=total_files, filename=iso_file.name))

        if final_zso.exists():
            print(t("skip_exists"))
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
                print(t("error_compression"))
                continue

            if not temp_zso.exists() or temp_zso.stat().st_size == 0:
                print(t("error_invalid_zso"))
                continue

            shutil.move(str(temp_zso), str(final_zso))
            print(t("ok_moved", path=final_zso))

            if keep_isos:
                print(t("ok_kept", filename=iso_file.name))
            else:
                iso_file.unlink()
                print(t("ok_deleted", filename=iso_file.name))

            converted_files += 1

        except Exception as error:
            print(t("error_exception", error=error))

    print(f"\n{t('summary_title')}")
    print(t("summary_found", total=total_files))
    print(t("summary_converted", converted=converted_files))
    print(t("summary_failed", failed=total_files - converted_files))
    iso_status = t("iso_kept") if keep_isos else t("iso_removed")
    print(t("summary_iso_status", status=iso_status))


if __name__ == "__main__":
    main()
