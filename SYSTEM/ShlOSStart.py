import subprocess
import os
import time
import sys
import platform
import psutil

sys.path.append(os.path.join(os.getcwd(), 'SYSTEM'))

# this tells the script what version of shellos this shit is
from version import __version__  

def verify_os():
    os_release = platform.release()
    os_version = platform.version()
    
    print(f"Detected OS: {platform.system()} {os_release} (Build {os_version})")

    if os_release in ["Vista", "XP", "2000", "ME", "98", "95", "NT", "CE"]:
        print("Error: ShellOS does not support Windows Vista or earlier.")
        sys.exit(1)
    
    # boo hoo windows 11 users
    if os_release == "11":
        print("[WARNING]: Windows 11 is not officially supported for ShellOS however, it should work. If you find any issues, please make a discussion at the ShellOS Github Repo.")

def verify_hardware():
    print("Verifying your hardware...")

    # Checks if you have a relevant CPU made anytime in the past decade
    cpu_arch = platform.machine().lower()
    if cpu_arch not in ["x86_64", "amd64", "intel64"]:
        print(f"Error: ShellOS requires a 64-bit CPU (x86_64/AMD64/Intel64). Detected: {cpu_arch}")
        sys.exit(1)

    # Inform this insane person they have a 32-Bit Python Interpreter on a 64-Bit CPU
    if sys.maxsize <= 2**32:
        print("[WARNING]: You are running a 32-bit Python interpreter on a 64-bit CPU. ShellOS may run, but 64-bit Python is recommended.")

    current_version = sys.version_info
    version_str = f"{current_version.major}.{current_version.minor}.{current_version.micro}"
    print(f"Python Interpreter Version: {version_str}")
    
    if current_version < (3, 12, 6):
        print("Error: ShellOS requires Python Interpreter version 3.12.6 or later.")
        sys.exit(1)

    cpu_name = platform.processor()
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
    cpu_cores = psutil.cpu_count(logical=False)

    ram_total = psutil.virtual_memory().total / (1024 ** 2)  # Convert to MB
    storage_info = psutil.disk_usage('/')
    storage_free = storage_info.free / (1024 ** 2)  # Convert to MB

    print("\nDetected Hardware:")
    print(f"CPU: {cpu_name}")
    print(f"CPU Architecture: {cpu_arch}")
    print(f"CPU Frequency: {cpu_freq:.2f} MHz")
    print(f"CPU Cores: {cpu_cores}")
    print(f"Total RAM: {ram_total:.2f} MB")
    print(f"Free Storage on Primary Device: {storage_free:.2f} MB\n")

    if cpu_freq < 300:
        print("Error: CPU frequency must be at least 300 MHz.")
        sys.exit(1)
    if cpu_cores < 1:
        print("Error: CPU must have at least 1 core.")
        sys.exit(1)
    if ram_total < 256:
        print("Error: System RAM must be at least 256 MB.")
        sys.exit(1)
    if storage_free < 256:
        print("Error: Free storage must be at least 256 MB.")
        sys.exit(1)

    print("Hardware requirements met.\n")

def main():
    print(f"Starting ShellOS {__version__}")
    time.sleep(2)

    verify_os()
    verify_hardware()

    shellos_script = os.path.join(os.getcwd(), 'SYSTEM', 'ShlOSCore.py')
    process = subprocess.Popen([sys.executable, shellos_script])
    process.wait()

if __name__ == "__main__":
    main()
