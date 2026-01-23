import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(title: str, subtitle: str = ""):
    clear_screen()
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}")
    print(f"  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print(f"{'=' * 60}{Colors.RESET}\n")

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_info(message: str):
    print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")

def get_image_bytes(file_path: str) -> Optional[bytes]:
    path = Path(file_path.strip('"'))
    if not path.exists():
        return None
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        print_error(f"Failed to read image: {e}")
        return None

def save_binary_file(file_path: Path, data: bytes) -> bool:
    try:
        with open(file_path, "wb") as f:
            f.write(data)
        print_success(f"Saved: {file_path.name}")
        return True
    except Exception as e:
        print_error(f"Failed to save file: {e}")
        return False

def open_file(path: Path):
    try:
        if os.name == 'nt':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.call(('open', path))
        else:
            subprocess.call(('xdg-open', path))
    except Exception as e:
        print_warning(f"Could not auto-open file: {e}")

def get_user_choice(prompt: str, valid_choices: list) -> str:
    while True:
        choice = input(f"{Colors.YELLOW}{prompt}{Colors.RESET}").strip().upper()
        if choice in [c.upper() for c in valid_choices]:
            return choice
        print_error(f"Invalid choice. Please choose from: {', '.join(valid_choices)}")

def confirm_action(message: str) -> bool:
    response = input(f"{Colors.YELLOW}{message} (Y/N): {Colors.RESET}").strip().upper()
    return response == 'Y'
