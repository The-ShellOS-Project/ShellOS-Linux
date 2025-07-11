import tkinter as tk
from tkinter import Label, Toplevel
from PIL import Image, ImageTk
import os
import sys
import platform
import pip
import webbrowser

# Determine the correct path to system version module
system_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'SYSTEM'))
sys.path.append(system_path)

try:
    from version import __version__
except ImportError as e:
    raise ImportError(f"Failed to import __version__. Ensure 'SYSTEM/version.py' exists and is accessible. Details: {e}")

def open_link(event):
    webbrowser.open_new("https://github.com/The-ShellOS-Project")

def about_program(parent):
    # Create the about window
    about_win = Toplevel(parent)
    about_win.title("About ShellOS")
    about_win.geometry("400x320")
    about_win.resizable(False, False)

    # Load and display the ShellOS logo
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ShlOSSys', 'resources', 'images', 'shellosverlogo.png'))
    if os.path.exists(logo_path):
        img = Image.open(logo_path)
        aspect_ratio = 15.12 / 4.25
        new_width = 150
        new_height = int(new_width / aspect_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        logo_label = Label(about_win, image=img)
        logo_label.image = img  # Keep a reference
        logo_label.pack(pady=10)
    else:
        error_label = Label(about_win, text="Image not found!", font=("Arial", 12), fg="red")
        error_label.pack(pady=10)

    # Get dynamic version info
    python_version = platform.python_version()
    pip_version = pip.__version__

    # Display version information
    info_text = f"""ShellOS
Version: {__version__}
Python {python_version}
Pip {pip_version}
"""
    info_label = Label(about_win, text=info_text, font=("Arial", 12), justify="center")
    info_label.pack(pady=(10, 2))

    # Add clickable GitHub link
    link_label = Label(
        about_win,
        text="https://github.com/The-ShellOS-Project",
        font=("Arial", 10, "underline"),
        fg="blue",
        cursor="hand2"
    )
    link_label.pack()
    link_label.bind("<Button-1>", open_link)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    about_program(root)
    root.mainloop()

if __name__ == "__main__":
    main()

