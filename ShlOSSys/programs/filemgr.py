import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess

ROOT_DIR = os.path.abspath(os.getcwd())

class ShellOSFileManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ShellOS File Manager")
        self.geometry("900x600")
        self.current_path = ROOT_DIR
        self.drag_data = []

        self.create_widgets()
        self.populate_tree()
        self.load_directory(self.current_path)

    def create_widgets(self):
        # Ribbon bar
        ribbon = tk.Frame(self)
        ribbon.pack(fill=tk.X)

        self.new_file_btn = tk.Button(ribbon, text="New File", command=self.new_file)
        self.new_folder_btn = tk.Button(ribbon, text="New Folder", command=self.new_folder)
        self.rename_btn = tk.Button(ribbon, text="Rename", command=self.rename_item)
        self.delete_btn = tk.Button(ribbon, text="Delete", command=self.delete_item)
        self.open_btn = tk.Button(ribbon, text="Open", command=self.open_item)

        for btn in [self.new_file_btn, self.new_folder_btn, self.rename_btn, self.delete_btn, self.open_btn]:
            btn.config(state=tk.DISABLED)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Address bar
        address_frame = tk.Frame(self)
        address_frame.pack(fill=tk.X)
        self.address_bar = tk.Entry(address_frame, state=tk.DISABLED)
        self.address_bar.pack(fill=tk.X, padx=5, pady=2)

        # Main area
        main = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        main.pack(fill=tk.BOTH, expand=1)

        # Directory Tree
        self.tree = ttk.Treeview(main)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        main.add(self.tree)

        # File Listbox
        self.file_list = tk.Listbox(main, selectmode=tk.EXTENDED)
        self.file_list.bind("<<ListboxSelect>>", self.update_buttons)
        self.file_list.bind("<Double-Button-1>", self.on_double_click)
        self.file_list.bind("<ButtonRelease-1>", self.correct_selection)
        main.add(self.file_list)

    def populate_tree(self):
        def insert_node(parent, path):
            try:
                for item in sorted(os.listdir(path)):
                    abs_path = os.path.join(path, item)
                    if os.path.isdir(abs_path):
                        node = self.tree.insert(parent, "end", text=item, open=False)
                        insert_node(node, abs_path)
            except Exception:
                pass

        self.tree.delete(*self.tree.get_children())
        root_node = self.tree.insert("", "end", text="ShellOS", open=True)
        insert_node(root_node, ROOT_DIR)

    def get_selected_list_items(self):
        return [self.file_list.get(i) for i in self.file_list.curselection()]

    def load_directory(self, path):
        self.current_path = path
        self.file_list.delete(0, tk.END)
        try:
            for item in sorted(os.listdir(path)):
                self.file_list.insert(tk.END, item)
        except Exception as e:
            messagebox.showerror("Error", str(e))

        relative_path = os.path.relpath(path, ROOT_DIR).replace("\\", "/")
        self.address_bar.config(state=tk.NORMAL)
        self.address_bar.delete(0, tk.END)
        self.address_bar.insert(0, relative_path if relative_path != "." else "ShellOS")
        self.address_bar.config(state=tk.DISABLED)
        self.update_buttons()

    def on_tree_select(self, event):
        selected = self.tree.focus()
        if selected:
            path = self.get_tree_path(selected)
            if path and os.path.isdir(path):
                self.load_directory(path)

    def get_tree_path(self, item):
        parts = []
        while item:
            parts.insert(0, self.tree.item(item)['text'])
            item = self.tree.parent(item)
        return os.path.join(ROOT_DIR, *parts[1:]) if parts else None

    def update_buttons(self, event=None):
        state = tk.NORMAL if self.file_list.curselection() else tk.DISABLED
        for btn in [self.rename_btn, self.delete_btn, self.open_btn]:
            btn.config(state=state)
        self.new_file_btn.config(state=tk.NORMAL)
        self.new_folder_btn.config(state=tk.NORMAL)

    def correct_selection(self, event):
        # Ensure click in empty space clears selection
        if self.file_list.nearest(event.y) >= self.file_list.size():
            self.file_list.selection_clear(0, tk.END)
            self.update_buttons()

    def new_file(self):
        new_path = filedialog.asksaveasfilename(initialdir=self.current_path)
        if new_path and new_path.startswith(ROOT_DIR):
            open(new_path, 'w').close()
            self.load_directory(self.current_path)

    def new_folder(self):
        name = filedialog.asksaveasfilename(initialdir=self.current_path)
        if name and name.startswith(ROOT_DIR):
            try:
                os.makedirs(name)
                self.load_directory(self.current_path)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def rename_item(self):
        selected = self.get_selected_list_items()
        if not selected:
            return
        old_path = os.path.join(self.current_path, selected[0])
        new_path = filedialog.asksaveasfilename(initialdir=self.current_path, initialfile=selected[0])
        if new_path and new_path.startswith(ROOT_DIR):
            os.rename(old_path, new_path)
            self.load_directory(self.current_path)

    def delete_item(self):
        for item in self.get_selected_list_items():
            path = os.path.join(self.current_path, item)
            try:
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    os.remove(path)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        self.load_directory(self.current_path)

    def open_item(self):
        for item in self.get_selected_list_items():
            path = os.path.join(self.current_path, item)
            self.try_open(path)

    def on_double_click(self, event):
        selection = self.file_list.curselection()
        if not selection:
            return
        name = self.file_list.get(selection[0])
        path = os.path.join(self.current_path, name)
        self.try_open(path)

    def try_open(self, path):
        try:
            if os.path.isdir(path):
                self.load_directory(path)
            elif os.path.isfile(path):
                if path.endswith(".txt"):
                    subprocess.Popen(["python", "ShlOSSys/programs/notepad.py", path])
                else:
                    os.startfile(path)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = ShellOSFileManager()
    app.mainloop()
