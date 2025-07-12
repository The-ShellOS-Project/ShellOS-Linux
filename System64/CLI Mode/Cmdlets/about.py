import os
import sys

# Determine the correct path to system version module
system_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'SYSTEM'))
sys.path.append(system_path)

try:
    from version import __version__ 
except ImportError as e:
    raise ImportError(f"Failed to import __version__. Ensure 'SYSTEM/version.py' exists and is accessible. Details: {e}")

def about_program():
    """Prints information about ShellOS to the console."""
    
    # Print version information
    info_text = f"""
    ShellOS
    Version: {__version__}
    Python 3.12.6
    Pip 24.2
    """
    print(info_text)

if __name__ == "__main__":
    about_program()
