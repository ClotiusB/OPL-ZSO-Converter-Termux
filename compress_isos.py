#!/usr/bin/env python3

import shutil
import subprocess
import sys
import os
from pathlib import Path
from time import sleep
import threading

ISO_DIR = Path("/sdcard/Download/Iso")
ZSO_DIR = Path("/sdcard/Download/Zso")

# Path to ziso.py
ZISO = "/data/data/com.termux/files/home/Open-PS2-Loader/pc/ziso.py"

# Compression level (0-12)
COMP_LEVEL = "2"

# Language setting (will be set by user)
LANGUAGE = None

# Colors (white only)
class Colors:
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Store conversion results
conversion_results = []


def clear_screen():
    """Clear terminal screen."""
    subprocess.run(['clear'], check=False)


def print_separator(length=50):
    """Print a decorative separator."""
    print(f"{Colors.WHITE}{'=' * length}{Colors.END}")


def format_size(bytes):
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"


# Translation dictionary
TRANSLATIONS = {
    "pt_BR": {
        "language_menu_title": "SELECAO DE IDIOMA",
        "language_separator": "==================================================",
        "language_select": "Escolha: ",
        "language_invalid": "[ERRO] Opcao invalida. Digite 1 ou 2.",
        
        "iso_handling_title": "PREFERENCIA DE TRATAMENTO ISO",
        "iso_option_1": "  [1] Manter arquivos ISO apos compressao",
        "iso_option_2": "  [2] Remover arquivos ISO apos compressao",
        "iso_separator": "==================================================",
        "iso_select": "Escolha: ",
        "iso_invalid": "[ERRO] Opcao invalida. Digite 1 ou 2.",
        
        "dir_not_found": "[ERRO] Diretorio nao encontrado: {path}",
        "no_iso_files": "[INFO] Nenhum arquivo ISO encontrado em {path}",
        "processing": "[{index}/{total}] Processando: {filename}",
        "skip_exists": "[PULAR] Arquivo ZSO ja existe no destino.",
        "error_compression": "[ERRO] Falha na compressao.",
        "error_invalid_zso": "[ERRO] Arquivo ZSO invalido gerado.",
        "error_move": "[ERRO] Falha ao mover arquivo para pasta Zso.",
        "ok_moved": "[OK] Arquivo movido com sucesso.",
        "ok_kept": "[OK] ISO mantida",
        "ok_deleted": "[OK] ISO deletada",
        "error_exception": "[ERRO] {error}",
        "compression_progress": "[COMPRIMINDO...]",
        
        "summary_title": "RESUMO FINAL",
        "summary_separator": "==================================================",
        "summary_found": "Arquivos ISO encontrados",
        "summary_converted": "Convertidos com sucesso",
        "summary_failed": "Falhados/Pulados",
        "summary_iso_status": "Arquivos ISO",
        "iso_kept": "Mantidos",
        "iso_removed": "Removidos",
        "starting": "INICIANDO COMPRESSAO",
        "detailed_results": "RESULTADOS DETALHADOS",
        "rom_name": "ROM",
        "iso_size_header": "Tamanho ISO",
        "zso_size_header": "Tamanho ZSO",
        "reduction_header": "Reducao",
    },
    "en_US": {
        "language_menu_title": "LANGUAGE SELECTION",
        "language_separator": "==================================================",
        "language_select": "Choose: ",
        "language_invalid": "[ERROR] Invalid choice. Please enter 1 or 2.",
        
        "iso_handling_title": "ISO HANDLING PREFERENCE",
        "iso_option_1": "  [1] Keep ISO files after compression",
        "iso_option_2": "  [2] Remove ISO files after compression",
        "iso_separator": "==================================================",
        "iso_select": "Choose: ",
        "iso_invalid": "[ERROR] Invalid choice. Please enter 1 or 2.",
        
        "dir_not_found": "[ERROR] Directory not found: {path}",
        "no_iso_files": "[INFO] No ISO files found in {path}",
        "processing": "[{index}/{total}] Processing: {filename}",
        "skip_exists": "[SKIP] ZSO file already exists in destination.",
        "error_compression": "[ERROR] Compression failed.",
        "error_invalid_zso": "[ERROR] Invalid ZSO file generated.",
        "error_move": "[ERROR] Failed to move file to Zso folder.",
        "ok_moved": "[OK] File moved successfully.",
        "ok_kept": "[OK] ISO kept",
        "ok_deleted": "[OK] ISO deleted",
        "error_exception": "[ERROR] {error}",
        "compression_progress": "[COMPRESSING...]",
        
        "summary_title": "SUMMARY",
        "summary_separator": "==================================================",
        "summary_found": "ISO files found",
        "summary_converted": "Successfully converted",
        "summary_failed": "Failed/Skipped",
        "summary_iso_status": "ISO files",
        "iso_kept": "Kept",
        "iso_removed": "Removed",
        "starting": "STARTING COMPRESSION",
        "detailed_results": "DETAILED RESULTS",
        "rom_name": "ROM",
        "iso_size_header": "ISO Size",
        "zso_size_header": "ZSO Size",
        "reduction_header": "Reduction",
    }
}

# Global progress variables
progress_percentage = 0
compression_active = False


def t(key, lang="pt_BR", **kwargs):
    """Get translated string for the specified language."""
    text = TRANSLATIONS[lang][key]
    if kwargs:
        return text.format(**kwargs)
    return text


def get_language():
    """Ask user to choose between Portuguese (Brazil) and English (American)."""
    clear_screen()
    while True:
        print_separator()
        print(f"{Colors.BOLD}{Colors.WHITE}SELECAO DE IDIOMA{Colors.END}")
        print_separator()
        print()
        print(f"{Colors.WHITE}  [1] Portugues Brasileiro{Colors.END}")
        print(f"{Colors.WHITE}  [2] English (American){Colors.END}")
        print()
        
        choice = input(f"{Colors.BOLD}{Colors.WHITE}> {Colors.END}").strip()
        
        if choice == "1":
            return "pt_BR"
        elif choice == "2":
            return "en_US"
        else:
            print(f"\n{Colors.WHITE}[ERRO] Opcao invalida. Digite 1 ou 2.{Colors.END}\n")
            sleep(1)


def get_user_preference(language):
    """Ask user if they want to keep or remove ISO files after compression."""
    while True:
        print(f"\n")
        print_separator()
        print(f"{Colors.BOLD}{Colors.WHITE}{t('iso_handling_title', lang=language)}{Colors.END}")
        print_separator()
        print()
        print(f"{Colors.WHITE}{t('iso_option_1', lang=language)}{Colors.END}")
        print(f"{Colors.WHITE}{t('iso_option_2', lang=language)}{Colors.END}")
        print()
        
        choice = input(f"{Colors.BOLD}{Colors.WHITE}> {Colors.END}").strip()
        
        if choice == "1":
            return True  # Keep ISO files
        elif choice == "2":
            return False  # Remove ISO files
        else:
            print(f"\n{Colors.WHITE}{t('iso_invalid', lang=language)}{Colors.END}\n")


def simulate_progress(process, total_time=100):
    """Simulate progress based on process execution."""
    global progress_percentage, compression_active
    
    start_time = __import__('time').time()
    
    while process.poll() is None and compression_active:
        elapsed = __import__('time').time() - start_time
        progress_percentage = min(int((elapsed / total_time) * 100), 99)
        sleep(0.1)
    
    if compression_active:
        progress_percentage = 100


def show_progress_screen(filename, language):
    """Show progress screen that updates with progress percentage."""
    global progress_percentage, compression_active
    
    bar_width = 40
    
    while compression_active and progress_percentage < 100:
        clear_screen()
        print_separator()
        print(f"{Colors.BOLD}{Colors.WHITE}{t('processing', lang=language, index='', total='', filename=filename)}{Colors.END}")
        print_separator()
        print()
        
        filled = int(bar_width * progress_percentage / 100)
        bar = '█' * filled + '░' * (bar_width - filled)
        
        print(f"{Colors.WHITE}[{bar}] {progress_percentage}%{Colors.END}")
        print()
        
        sleep(0.2)
    
    if progress_percentage == 100:
        clear_screen()
        print_separator()
        print(f"{Colors.BOLD}{Colors.WHITE}{t('processing', lang=language, index='', total='', filename=filename)}{Colors.END}")
        print_separator()
        print()
        filled = bar_width
        bar = '█' * filled
        print(f"{Colors.WHITE}[{bar}] 100%{Colors.END}")
        print()
        sleep(0.5)


def move_file_safely(src, dst):
    """Safely move file using copy and delete or using system command."""
    try:
        # Try using shutil.move first
        shutil.move(str(src), str(dst))
        return True
    except Exception as e1:
        try:
            # If shutil.move fails, try cp and rm
            subprocess.run(['cp', str(src), str(dst)], check=True, capture_output=True)
            os.remove(str(src))
            return True
        except Exception as e2:
            return False


def main():
    global LANGUAGE, progress_percentage, compression_active, conversion_results
    LANGUAGE = get_language()
    
    clear_screen()
    
    # Ensure ZSO_DIR exists
    try:
        ZSO_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"{Colors.WHITE}[ERRO] Falha ao criar diretorio {ZSO_DIR}: {e}{Colors.END}")
        return

    if not ISO_DIR.exists():
        print_separator()
        print(f"{Colors.WHITE}{t('dir_not_found', lang=LANGUAGE, path=ISO_DIR)}{Colors.END}")
        print_separator()
        return

    iso_files = sorted(ISO_DIR.glob("*.iso"))

    if not iso_files:
        print_separator()
        print(f"{Colors.WHITE}{t('no_iso_files', lang=LANGUAGE, path=ISO_DIR)}{Colors.END}")
        print_separator()
        return

    keep_isos = get_user_preference(LANGUAGE)

    clear_screen()
    print(f"\n")
    print_separator()
    print(f"{Colors.BOLD}{Colors.WHITE}{t('starting', lang=LANGUAGE)}{Colors.END}")
    print_separator()
    print()
    sleep(1)

    total_files = len(iso_files)
    converted_files = 0

    for index, iso_file in enumerate(iso_files, start=1):
        game_name = iso_file.stem

        temp_zso = ISO_DIR / f"{game_name}.zso"
        final_zso = ZSO_DIR / f"{game_name}.zso"

        if final_zso.exists():
            clear_screen()
            print_separator()
            print(f"{Colors.WHITE}{t('processing', lang=LANGUAGE, index=index, total=total_files, filename=iso_file.name)}{Colors.END}")
            print_separator()
            print()
            print(f"{Colors.WHITE}{t('skip_exists', lang=LANGUAGE)}{Colors.END}")
            print()
            sleep(1)
            continue

        iso_size = iso_file.stat().st_size
        
        command = [
            "python",
            ZISO,
            "-c",
            COMP_LEVEL,
            str(iso_file),
            str(temp_zso)
        ]

        try:
            # Reset progress
            progress_percentage = 0
            compression_active = True
            
            # Start process
            process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Start progress simulation thread
            progress_thread = threading.Thread(target=simulate_progress, args=(process, 100))
            progress_thread.daemon = True
            progress_thread.start()
            
            # Show progress screen
            show_progress_screen(iso_file.name, LANGUAGE)
            
            # Wait for process to complete
            process.wait()
            compression_active = False

            if process.returncode != 0:
                clear_screen()
                print_separator()
                print(f"{Colors.WHITE}{t('processing', lang=LANGUAGE, index=index, total=total_files, filename=iso_file.name)}{Colors.END}")
                print_separator()
                print()
                print(f"{Colors.WHITE}{t('error_compression', lang=LANGUAGE)}{Colors.END}")
                print()
                sleep(1)
                continue

            if not temp_zso.exists() or temp_zso.stat().st_size == 0:
                clear_screen()
                print_separator()
                print(f"{Colors.WHITE}{t('processing', lang=LANGUAGE, index=index, total=total_files, filename=iso_file.name)}{Colors.END}")
                print_separator()
                print()
                print(f"{Colors.WHITE}{t('error_invalid_zso', lang=LANGUAGE)}{Colors.END}")
                print()
                sleep(1)
                continue

            zso_size = temp_zso.stat().st_size
            reduction_percent = ((iso_size - zso_size) / iso_size) * 100

            # Move file safely
            if not move_file_safely(temp_zso, final_zso):
                clear_screen()
                print_separator()
                print(f"{Colors.WHITE}{t('processing', lang=LANGUAGE, index=index, total=total_files, filename=iso_file.name)}{Colors.END}")
                print_separator()
                print()
                print(f"{Colors.WHITE}{t('error_move', lang=LANGUAGE)}{Colors.END}")
                print()
                sleep(1)
                continue

            clear_screen()
            print_separator()
            print(f"{Colors.WHITE}{t('processing', lang=LANGUAGE, index=index, total=total_files, filename=iso_file.name)}{Colors.END}")
            print_separator()
            print()
            print(f"{Colors.WHITE}{t('ok_moved', lang=LANGUAGE)}{Colors.END}")

            if keep_isos:
                print(f"{Colors.WHITE}{t('ok_kept', lang=LANGUAGE)}{Colors.END}")
            else:
                iso_file.unlink()
                print(f"{Colors.WHITE}{t('ok_deleted', lang=LANGUAGE)}{Colors.END}")

            # Store result
            conversion_results.append({
                'name': game_name,
                'iso_size': iso_size,
                'zso_size': zso_size,
                'reduction': reduction_percent
            })

            converted_files += 1
            sleep(1)

        except Exception as error:
            clear_screen()
            print_separator()
            print(f"{Colors.WHITE}{t('processing', lang=LANGUAGE, index=index, total=total_files, filename=iso_file.name)}{Colors.END}")
            print_separator()
            print()
            print(f"{Colors.WHITE}{t('error_exception', lang=LANGUAGE, error=error)}{Colors.END}")
            print()
            sleep(1)

    clear_screen()
    print_separator()
    print(f"{Colors.BOLD}{Colors.WHITE}{t('summary_title', lang=LANGUAGE)}{Colors.END}")
    print_separator()
    print()
    
    # Display summary in columns
    iso_status = t("iso_kept", lang=LANGUAGE) if keep_isos else t("iso_removed", lang=LANGUAGE)
    
    line1 = f"{t('summary_found', lang=LANGUAGE)}: {total_files}"
    line2 = f"{t('summary_converted', lang=LANGUAGE)}: {converted_files}"
    line3 = f"{t('summary_failed', lang=LANGUAGE)}: {total_files - converted_files}"
    line4 = f"{t('summary_iso_status', lang=LANGUAGE)}: {iso_status}"
    
    # Calculate column widths (approximately 25 characters each for 2 columns)
    col_width = 40
    
    print(f"{Colors.WHITE}{line1:<{col_width}}{line2:<{col_width}}{Colors.END}")
    print(f"{Colors.WHITE}{line3:<{col_width}}{line4:<{col_width}}{Colors.END}")
    print()
    
    # Display detailed results
    if conversion_results:
        print_separator()
        print(f"{Colors.BOLD}{Colors.WHITE}{t('detailed_results', lang=LANGUAGE)}{Colors.END}")
        print_separator()
        print()
        
        # Print each result
        for result in conversion_results:
            rom_name = result['name']
            iso_size_str = format_size(result['iso_size'])
            zso_size_str = format_size(result['zso_size'])
            reduction_str = f"{result['reduction']:.1f}%"
            
            print(f"{Colors.WHITE}{rom_name}{Colors.END}")
            print(f"{Colors.WHITE}  {t('iso_size_header', lang=LANGUAGE)}: {iso_size_str}{Colors.END}")
            print(f"{Colors.WHITE}  {t('zso_size_header', lang=LANGUAGE)}: {zso_size_str}{Colors.END}")
            print(f"{Colors.WHITE}  {t('reduction_header', lang=LANGUAGE)}: {reduction_str}{Colors.END}")
            print()
    
    print_separator()
    print()


if __name__ == "__main__":
    main()
        
