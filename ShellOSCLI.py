import subprocess
import sys
import os
import importlib.util

def is_package_installed(package_name):
    """Check if a package is installed without using deprecated pkg_resources."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def check_and_install_requirements():
    """Checks if required packages are installed; installs them if missing."""
    requirements_file = os.path.join(os.getcwd(), 'requirements.txt')
    
    if not os.path.isfile(requirements_file):
        print("requirements.txt file not found.")
        sys.exit(1)
    
    with open(requirements_file, 'r') as file:
        required_packages = [line.strip().split('=')[0] for line in file if line.strip()]
    
    missing_packages = [pkg for pkg in required_packages if not is_package_installed(pkg)]
    
    if missing_packages:
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("All required packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install required packages: {e}")
            sys.exit(1)
    else:
        print("All required packages are already installed.")

def run_shloscli():
    """Runs the ShlOSCLI.py script after setting up the correct path."""
    project_root = os.path.abspath(os.path.dirname(__file__))

    system_path = os.path.join(project_root, "SYSTEM")
    
    if not os.path.isdir(system_path):
        print(f"Error: SYSTEM directory not found at {system_path}")
        sys.exit(1)

    version_path = os.path.join(system_path, "version.py")

    if not os.path.isfile(version_path):
        print(f"Error: version.py not found in {system_path}")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("version", version_path)
    version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version)

    __version__ = version.__version__

    print(f"ShellOS CLI version: {__version__}")

    shlos_start_path = os.path.join(project_root, "CLI Mode", "ShlOSCLI.py")

    if not os.path.isfile(shlos_start_path):
        print(f"Error: 'ShlOSCLI.py' not found at expected location: {shlos_start_path}")
        sys.exit(1)

    try:
        subprocess.check_call([sys.executable, shlos_start_path])
    except subprocess.CalledProcessError as e:
        print(f"Failed to run ShlOSCLI.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_and_install_requirements()
    run_shloscli()
