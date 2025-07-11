import subprocess
import sys
import os

def install_requirements():
    """Installs required packages from requirements.txt."""
    requirements_file = os.path.join(os.getcwd(), 'requirements.txt')
    if os.path.isfile(requirements_file):
        try:
            print("Installing required packages...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
            print("All required packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install required packages: {e}")
            sys.exit(1)
    else:
        print("requirements.txt file not found.")
        sys.exit(1)

    try:
        print("Running ShlOSStart.py...")
        shlos_start_path = os.path.join(os.getcwd(), 'SYSTEM', 'ShlOSStart.py')
        if os.path.isfile(shlos_start_path):
            subprocess.check_call([sys.executable, shlos_start_path])
            print("ShlOSStart.py ran successfully.")
        else:
            print("ShlOSStart.py not found.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run ShlOSStart.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
