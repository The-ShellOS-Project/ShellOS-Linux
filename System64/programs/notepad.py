import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

class ShellOSNotepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ShellOS Notepad")
        self.geometry("600x400")
        self.current_file = None

        # Dark mode colors
        BACKGROUND_COLOR = "#191919"  # Very dark grey
        FOREGROUND_COLOR = "#FFFFFF"  # White
        TEXT_AREA_BG = "#2B2B2B"      # Slightly lighter dark grey for text area
        TEXT_AREA_FG = "#FFFFFF"      # White for text area text
        STATUS_BAR_BG = "#141414"     # Darker grey for status bar
        STATUS_BAR_FG = "#FFFFFF"     # White for status bar text

        self.config(bg=BACKGROUND_COLOR)

        # Menu bar
        menubar = tk.Menu(self, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
        file_menu.add_command(label="Open", command=self.view_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=menubar)

        # Text area
        self.text = tk.Text(self, undo=True, wrap=tk.WORD, bg=TEXT_AREA_BG, fg=TEXT_AREA_FG, insertbackground=FOREGROUND_COLOR)
        self.text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_label = tk.Label(self, text="Ready", anchor="w", bg=STATUS_BAR_BG, fg=STATUS_BAR_FG)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def view_file(self):
        file_path = filedialog.askopenfilename(
            initialdir="System64/Documents",
            title="Open File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.open_file(file_path)

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w') as f:
                    f.write(self.text.get(1.0, tk.END).rstrip())
                self.status_label.config(text=f"Saved: {os.path.basename(self.current_file)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            initialdir="System64/Documents",
            title="Save File As",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.current_file = file_path
            self.save_file()

    def open_file(self, path):
        try:
            with open(path, 'r') as f:
                content = f.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, content)
            self.current_file = path
            self.status_label.config(text=f"Opened: {os.path.basename(path)}")
        except FileNotFoundError:
            self.text.delete(1.0, tk.END)
            self.status_label.config(text="File not found.")

    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

if __name__ == "__main__":
    app = ShellOSNotepad()
    if len(sys.argv) > 1:
        app.open_file(sys.argv[1])
    app.mainloop()