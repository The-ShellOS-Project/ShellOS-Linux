import tkinter as tk
from tkinter import scrolledtext
import os
import subprocess
import threading

class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal")

        self.cwd = os.getcwd()

        icon_path = self.resolve_path("ShellOS/SYSTEM/Graphical_Shell/icons/terminal.png")
        if os.path.exists(icon_path):
            icon_image = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, icon_image)
        else:
            print(f"Warning: Icon file not found at {icon_path}")


        self.terminal = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, bg="black", fg="white",
            insertbackground="white", font=("Consolas", 12),
            undo=True
        )
        self.terminal.pack(expand=True, fill=tk.BOTH)

        self.terminal.bind("<Return>", self.process_command)
        self.terminal.bind("<BackSpace>", self.prevent_backspace)
        self.terminal.bind("<Key>", self.prevent_edit_before_prompt)

        self.terminal.tag_config("prompt", foreground="white")
        self.terminal.tag_config("shlos_purple", foreground="#260F33")

        self.command_locations = {
            "help": self.resolve_path("ShellOS/ShlOSSys/Cmdlets/help.py"),
            "notepad": self.resolve_path("ShellOS/ShlOSSys/Programs/Notepad.py"),
            "sysfetch": self.resolve_path("ShellOS/ShlOSSys/Programs/Sysfetch.py"),
            "about": self.resolve_path("ShellOS/ShlOSSys/Programs/About.py"),
            "calc": self.resolve_path("ShellOS/ShlOSSys/Programs/Calc.py"),
            "echo": self.resolve_path("ShellOS/ShlOSSys/Cmdlets/echo.py"),
            "listdir": self.resolve_path("ShellOS/ShlOSSys/Cmdlets/listdir.py"),
            "shlzip": self.resolve_path("ShellOS/ShlOSSys/programs/shlzip.py"),
            "spm": self.resolve_path("ShellOS/ShlOSSys/programs/SPM.py"),
        }

        self.insert_prompt()

    def resolve_path(self, relative_path):
        current_dir = os.path.abspath(os.getcwd())
        shellos_index = current_dir.find("ShellOS")

        if shellos_index == -1:
            print("Error: 'ShellOS' directory not found in path.")
            return relative_path

        shellos_root = current_dir[:shellos_index] + "ShellOS"
        return os.path.join(shellos_root, *relative_path.split("/")[1:])

    def insert_prompt(self):
        prompt = f"{self.cwd}>"
        self.terminal.insert(tk.END, prompt, "prompt")
        self.terminal.mark_set("insert", tk.END)
        self.prompt_index = self.terminal.index("insert")

    def process_command(self, event):
        line_start = self.terminal.index("insert linestart")
        line_end = self.terminal.index("insert lineend")
        line_text = self.terminal.get(line_start, line_end).strip()

        if ">" in line_text:
            command_text = line_text.split(">", 1)[-1].strip()
        else:
            command_text = line_text.strip()

        self.terminal.insert(tk.END, "\n")
        threading.Thread(target=self.execute_command, args=(command_text,), daemon=True).start()
        return "break"

    def prevent_backspace(self, event):
        if self.terminal.compare("insert", "<=", self.prompt_index):
            return "break"
        return None

    def prevent_edit_before_prompt(self, event):
        if event.keysym in ("Left", "BackSpace") and self.terminal.compare("insert", "<=", self.prompt_index):
            return "break"
        return None

    def execute_command(self, command_text):
        parts = command_text.split()
        command = parts[0].lower() if parts else ""
        args = parts[1:]

        if command == "cd":
            self.root.after(0, lambda: self.change_directory(args))
            self.root.after(0, self.insert_prompt)
            return
        elif command == "clear":
            self.root.after(0, lambda: self.terminal.delete("1.0", tk.END))
            self.root.after(0, self.insert_prompt)
            return
        elif command in self.command_locations:
            self.run_file(self.command_locations[command], args)
            return
        else:
            # Try to find matching .py, .bat, .sh in Programs or Cmdlets
            search_dirs = [
                self.resolve_path("ShellOS/ShlOSSys/Programs"),
                self.resolve_path("ShellOS/ShlOSSys/Cmdlets")
            ]
            extensions = [".py", ".bat", ".sh"]

            for directory in search_dirs:
                for ext in extensions:
                    possible_file = os.path.join(directory, command + ext)
                    if os.path.isfile(possible_file) and possible_file not in self.command_locations.values():
                        self.run_file(possible_file, args)
                        return

        # If not found, try system command
        try:
            process = subprocess.Popen(
                command_text, shell=True, cwd=self.cwd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            for line in process.stdout:
                self.root.after(0, lambda line=line: self.insert_colored_line(line))
        except Exception as e:
            self.root.after(0, lambda: self.terminal.insert(tk.END, f"Shell error: {str(e)}\n"))

        self.root.after(0, self.insert_prompt)
        self.root.after(0, lambda: self.terminal.see(tk.END))

    def change_directory(self, args):
        if not args:
            self.cwd = os.path.expanduser("~")
        else:
            new_path = os.path.abspath(os.path.join(self.cwd, " ".join(args)))
            if os.path.isdir(new_path):
                self.cwd = new_path
            else:
                self.terminal.insert(tk.END, f"cd: no such directory: {new_path}\n")

    def insert_colored_line(self, line):
        if line.startswith(">>"):
            parts = line[2:].split(":", 1)
            if len(parts) == 2:
                label, value = parts
                self.terminal.insert(tk.END, f"{label.strip()}:", "shlos_purple")
                self.terminal.insert(tk.END, f"{value}\n")
                return
        self.terminal.insert(tk.END, line)

    def run_file(self, file_path, args):
        if not os.path.isfile(file_path):
            self.root.after(0, lambda: self.terminal.insert(tk.END, f"Error: File '{file_path}' not found.\n"))
            self.root.after(0, self.insert_prompt)
            return

        def task():
            try:
                if file_path.endswith(".py"):
                    cmd = ["python", file_path] + args
                elif file_path.endswith(".bat"):
                    cmd = [file_path] + args
                elif file_path.endswith(".sh"):
                    cmd = ["bash", file_path] + args
                else:
                    self.root.after(0, lambda: self.terminal.insert(tk.END, "Error: Unsupported file type.\n"))
                    self.root.after(0, self.insert_prompt)
                    return

                result = subprocess.run(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, cwd=self.cwd, shell=False, timeout=60
                )

                if result.stdout:
                    for line in result.stdout.splitlines():
                        self.root.after(0, lambda line=line: self.insert_colored_line(line + "\n"))
                if result.stderr:
                    self.root.after(0, lambda: self.terminal.insert(tk.END, f"Error: {result.stderr}\n"))

            except subprocess.TimeoutExpired:
                self.root.after(0, lambda: self.terminal.insert(tk.END, "Error: Process timed out.\n"))
            except Exception as e:
                self.root.after(0, lambda: self.terminal.insert(tk.END, f"Error: {str(e)}\n"))

            self.root.after(0, self.insert_prompt)
            self.root.after(0, lambda: self.terminal.see(tk.END))

        threading.Thread(target=task, daemon=True).start()


# Run the app
root = tk.Tk()
app = TerminalApp(root)
root.geometry("1020x642")
root.mainloop()
