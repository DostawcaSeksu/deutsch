import subprocess
import sys

def clear_screen():
    """Clears the console screen in a platform-independent way."""
    command = 'cls' if sys.platform == 'win32' else 'clear'
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception:
        print("\n" * 100)