import os
import platform
import time
import subprocess
import psutil

def get_version():
    try:
        version_path = os.path.join("SYSTEM", "version.py")
        spec = {}
        with open(version_path, "r") as f:
            exec(f.read(), spec)
        return spec.get("__version__", "Unknown")
    except Exception:
        return "Unknown"

def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def get_pip_version():
    try:
        output = subprocess.check_output(["pip", "--version"], text=True)
        return output.split()[1]
    except Exception:
        return "Unknown"

def get_cpu_info():
    try:
        cpu = platform.processor()
        freq = psutil.cpu_freq()
        if freq:
            freq_str = f"{freq.current:.2f} GHz"
        else:
            freq_str = "Unknown"
        return f"{cpu} @ {freq_str}"
    except Exception:
        return "Unknown"

def get_memory_usage():
    try:
        mem = psutil.virtual_memory()
        used_gb = mem.used / (1024 ** 3)
        total_gb = mem.total / (1024 ** 3)
        return f"{used_gb:.2f} GB / {total_gb:.2f} GB"
    except Exception:
        return "Unknown"

def main():
    version = get_version()
    print(f"OS: ShellOS {version}")
    print("Core: 2.0")
    print(f"Uptime: {get_uptime()}")
    print(f"Python: {platform.python_version()}")
    print(f"Pip: {get_pip_version()}")
    print("Shell: ShellOS Terminal")
    print(f"CPU: {get_cpu_info()}")
    print(f"Memory: {get_memory_usage()}")

if __name__ == "__main__":
    main()
