import os
import platform
import sys
import importlib.util
import subprocess

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ensure SYSTEM directory is added to Python's module search path
system_path = os.path.join(project_root, "SYSTEM")

if not os.path.isdir(system_path):
    print(f"Error: SYSTEM directory not found at {system_path}")
    sys.exit(1)

# Manually load version.py from SYSTEM folder
version_path = os.path.join(system_path, "version.py")

if not os.path.isfile(version_path):
    print(f"Error: version.py not found in {system_path}")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("version", version_path)
version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version)

__version__ = version.__version__

# Define the directories where command files are located
command_dirs = [
    os.path.join(project_root, "commands"),  # Main command directory
    os.path.join(system_path, "builtins"),   # Built-in commands
]

# Store available commands (without extensions)
commands = {}

def add_command(name, path):
    commands[name.lower()] = path

# Manually add your commands (no need to scan directories)
add_command("Notepad", "CLI Mode/programs/notepad.py")
add_command("example", "CLI Mode/Cmdlets/Sysfetch.py")
add_command("About", "CLI Mode/Cmdlets/About.py")
add_command("Programs", "CLI Mode/Cmdlets/Programs.py")
# add_command("example", "example.py")

# Optionally, you can add more commands manually like this
# add_command("mycommand", "mycommand.py")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(f"Crypticsoft ShellOS {__version__}")

def show_help():
    print("\nAvailable Commands and Programs:")
    print("Help           Displays this, duh.")
    print("About          Displays ShellOS Information.")
    print("Sysfetch       Displays Device Information.")
    print("Programs       Displays a list of Programs.")

def execute_command(command):
    command = command.lower()
    if command in commands:
        cmd_path = commands[command]
        ext = os.path.splitext(cmd_path)[1]
        
        if ext == ".py":
            subprocess.run(["python", cmd_path])
        elif ext == ".bat" and os.name == "nt":
            subprocess.run([cmd_path], shell=True)
        elif ext == ".sh" and os.name != "nt":
            subprocess.run(["bash", cmd_path])
        else:
            print(f"Unsupported file type: {ext}")
    else:
        print(f"Unknown command: {command}. Type 'help' for a list of commands.")

def main():
    clear_screen()
    show_banner()
    
    while True:
        command = input("ShellOS>").strip().lower()
        
        if command == "help":
            show_help()
        elif command == "clear":
            clear_screen()
            show_banner()
        elif command == "exit":
            print("Exiting...")
            break
        else:
            execute_command(command)
            
if __name__ == "__main__":
    main()
