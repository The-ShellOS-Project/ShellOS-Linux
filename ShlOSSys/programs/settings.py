import tkinter as tk
from tkinter import ttk
import os
import subprocess
import json

class SettingsPanel:
    def __init__(self, master):
        # Set up the main window
        self.master = master
        self.master.title("Settings Panel")
        self.master.geometry("600x400")

        # Header
        ttk.Label(
            master,
            text="Settings Panel",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Frame for applet list
        self.settings_frame = tk.Frame(master, bg="#f4f4f4")
        self.settings_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # List of applets
        self.applets = []
        self.load_applets()

        # Add applets to UI
        self.display_applets()

    def load_applets(self):
        """Load applets dynamically from a predefined list."""
        # Define applets manually for now with the correct path for the background settings script
        self.applets = [
            ("Time and Date", "ShlOSSys/SettingsApplets/timeanddate.py"),
            ("Background Settings", os.path.join("ShellOS", "SYSTEM", "Graphical_Shell", "Backgroundsettings.py")),  # Updated path
        ]

    def display_applets(self):
        """Display the list of applets in the UI."""
        row = 0
        for applet_name, applet_path in self.applets:
            ttk.Label(self.settings_frame, text=applet_name, font=("Arial", 12)).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            open_button = ttk.Button(
                self.settings_frame,
                text="Open",
                command=lambda path=applet_path: self.open_applet(path)
            )
            open_button.grid(row=row, column=1, padx=10, pady=5)
            row += 1

    def open_applet(self, path):
        """Open the applet by running the associated file."""
        try:
            # Use subprocess to run the applet
            subprocess.Popen(["python", path], shell=True)
            print(f"Opened applet: {path}")
        except Exception as e:
            print(f"Failed to open applet: {e}")

# Run the Settings Panel
if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsPanel(root)
    root.mainloop()
