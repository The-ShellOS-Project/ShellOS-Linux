import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys
import platform

# Define dark mode colors
BG_COLOR = "#191919"  # Dark background
FG_COLOR = "white"   # White text for general info
ACCENT_COLOR = "#333333" # A slightly lighter dark for accents/elements
BUTTON_HOVER_BG = "#2a2a2a" # Darker hover for buttons
SELECTED_BG = "#444444" # Background for selected items
SELECTED_FG = "white" # Foreground for selected items
DISABLED_BG = "#0f0f0f" # Even darker for disabled elements
DISABLED_FG = "#666666" # Greyed out text for disabled elements
BORDER_COLOR = "#555555" # Light grey for borders/separators

# --- MODIFICATION START ---
# Define ROOT_DIR to be the 'ShellOS' folder, two levels up from the script's location
APP_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__)) # C:\...\ShellOS\System64\Programs
# Go up one level (from Programs to System64)
SYSTEM64_DIR = os.path.dirname(APP_SCRIPT_DIR) # C:\...\ShellOS\System64
# Go up another level (from System64 to ShellOS)
ROOT_DIR = os.path.dirname(SYSTEM64_DIR) # C:\...\ShellOS

# Ensure the ROOT_DIR exists
os.makedirs(ROOT_DIR, exist_ok=True)
# --- MODIFICATION END ---

class ShellOSFileManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ShellOS File Manager")
        self.geometry("900x600")
        self.config(bg=BG_COLOR) # Apply background to the root window

        self.current_path = ROOT_DIR
        self.drag_data = []

        self.apply_dark_theme() # Apply the dark theme globally

        self.create_widgets()
        self.populate_tree()
        self.load_directory(self.current_path)

    def apply_dark_theme(self):
        """Applies a dark theme to Tkinter and ttk widgets."""
        # Configure Tkinter widget defaults
        self.option_add("*Background", BG_COLOR)
        self.option_add("*Foreground", FG_COLOR)
        self.option_add("*Button.background", ACCENT_COLOR)
        self.option_add("*Button.foreground", FG_COLOR)
        self.option_add("*Button.activeBackground", BUTTON_HOVER_BG)
        self.option_add("*Button.activeForeground", FG_COLOR)
        self.option_add("*Entry.background", ACCENT_COLOR)
        self.option_add("*Entry.foreground", FG_COLOR)
        self.option_add("*Entry.insertBackground", FG_COLOR) # Caret color
        self.option_add("*Listbox.background", ACCENT_COLOR)
        self.option_add("*Listbox.foreground", FG_COLOR)
        self.option_add("*Listbox.selectBackground", SELECTED_BG)
        self.option_add("*Listbox.selectForeground", SELECTED_FG)
        self.option_add("*Frame.background", BG_COLOR)
        self.option_add("*PanedWindow.background", BG_COLOR)

        # Configure ttk styles
        style = ttk.Style(self)
        style.theme_use("clam") # 'clam' theme provides better customization options

        # General style for all widgets
        style.configure(".", background=BG_COLOR, foreground=FG_COLOR, bordercolor=BORDER_COLOR)

        # Style for Treeview
        style.configure("Treeview",
                        background=ACCENT_COLOR,
                        foreground=FG_COLOR,
                        fieldbackground=ACCENT_COLOR,
                        bordercolor=BORDER_COLOR,
                        lightcolor=ACCENT_COLOR, # Light part of the element's border
                        darkcolor=ACCENT_COLOR) # Dark part of the element's border

        style.map("Treeview",
                  background=[("selected", SELECTED_BG)],
                  foreground=[("selected", SELECTED_FG)])

        # Style for Treeview Headings
        style.configure("Treeview.Heading",
                        background=ACCENT_COLOR,
                        foreground=FG_COLOR,
                        font=("TkDefaultFont", 10, "bold"),
                        relief="flat") # Use 'flat' for a modern look
        style.map("Treeview.Heading",
                  background=[("active", BUTTON_HOVER_BG)]) # Hover effect for heading

        # Style for Scrollbars (used by Treeview and Listbox implicitly)
        style.configure("Vertical.TScrollbar",
                        background=ACCENT_COLOR,
                        troughcolor=BG_COLOR,
                        bordercolor=BORDER_COLOR,
                        arrowcolor=FG_COLOR)
        style.map("Vertical.TScrollbar",
                  background=[("active", BUTTON_HOVER_BG)],
                  arrowcolor=[("active", FG_COLOR)])

        style.configure("Horizontal.TScrollbar",
                        background=ACCENT_COLOR,
                        troughcolor=BG_COLOR,
                        bordercolor=BORDER_COLOR,
                        arrowcolor=FG_COLOR)
        style.map("Horizontal.TScrollbar",
                  background=[("active", BUTTON_HOVER_BG)],
                  arrowcolor=[("active", FG_COLOR)])

        # Style for PanedWindow sash
        style.configure("Panedwindow", background=BORDER_COLOR)
        style.configure("Panedwindow.sash", background=BORDER_COLOR)
        style.map("Panedwindow.sash", background=[("active", FG_COLOR)]) # Sash color when dragging

    def create_widgets(self):
        """Creates all the GUI widgets for the file manager."""
        # Ribbon bar
        ribbon = tk.Frame(self, bd=1, relief=tk.RAISED, bg=BG_COLOR) # Added border and relief
        ribbon.pack(fill=tk.X, padx=5, pady=5)

        # Buttons (configured manually for consistency as default style might not apply to all states)
        button_common_kwargs = {
            "bg": ACCENT_COLOR,
            "fg": FG_COLOR,
            "activebackground": BUTTON_HOVER_BG,
            "activeforeground": FG_COLOR,
            "relief": tk.FLAT, # Flat buttons for modern look
            "highlightbackground": BG_COLOR, # For border color on some OS
            "highlightthickness": 0,
            "bd": 0, # Remove default border
            "padx": 10,
            "pady": 5
        }

        self.new_file_btn = tk.Button(ribbon, text="New File", command=self.new_file, **button_common_kwargs)
        self.new_folder_btn = tk.Button(ribbon, text="New Folder", command=self.new_folder, **button_common_kwargs)
        self.rename_btn = tk.Button(ribbon, text="Rename", command=self.rename_item, **button_common_kwargs)
        self.delete_btn = tk.Button(ribbon, text="Delete", command=self.delete_item, **button_common_kwargs)
        self.open_btn = tk.Button(ribbon, text="Open", command=self.open_item, **button_common_kwargs)

        for btn in [self.new_file_btn, self.new_folder_btn, self.rename_btn, self.delete_btn, self.open_btn]:
            btn.config(state=tk.DISABLED)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Address bar
        address_frame = tk.Frame(self, bg=BG_COLOR)
        address_frame.pack(fill=tk.X, padx=5, pady=2)
        self.address_bar = tk.Entry(
            address_frame,
            state=tk.DISABLED,
            bg=ACCENT_COLOR,
            fg=FG_COLOR,
            insertbackground=FG_COLOR, # Caret color
            disabledbackground=DISABLED_BG,
            disabledforeground=DISABLED_FG,
            relief=tk.FLAT, # Flat entry for modern look
            highlightbackground=BORDER_COLOR, # Border color
            highlightthickness=1,
            bd=0
        )
        self.address_bar.pack(fill=tk.X, expand=True, padx=5, pady=2)

        # Main area - PanedWindow
        main = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=BG_COLOR, sashrelief=tk.RAISED, sashwidth=5)
        main.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        # Directory Tree
        self.tree = ttk.Treeview(main, show="tree headings")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Add a scrollbar to the treeview
        tree_scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        tree_scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        main.add(self.tree, width=300)

        # File Listbox
        self.file_list = tk.Listbox(
            main,
            selectmode=tk.EXTENDED,
            bg=ACCENT_COLOR,
            fg=FG_COLOR,
            selectbackground=SELECTED_BG,
            selectforeground=SELECTED_FG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            bd=0,
            activestyle="dotbox"
        )
        # Bind the ListboxSelect event
        self.file_list.bind("<<ListboxSelect>>", self.on_listbox_select)
        # Bind double-click
        self.file_list.bind("<Double-Button-1>", self.on_double_click)

        # Add a scrollbar to the listbox
        list_scrollbar = ttk.Scrollbar(self.file_list, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=list_scrollbar.set)
        list_scrollbar.pack(side="right", fill="y")
        self.file_list.pack(side="left", fill="both", expand=True)
        main.add(self.file_list)

    def populate_tree(self):
        """Populates the directory treeview with the file system structure."""
        def insert_node(parent, path):
            """Recursively inserts initial directory nodes into the treeview with placeholders."""
            try:
                for item in sorted(os.listdir(path)):
                    abs_path = os.path.join(path, item)
                    # Only insert if it's a directory and within ROOT_DIR
                    if os.path.isdir(abs_path) and os.path.abspath(abs_path).startswith(ROOT_DIR):
                        node_id = self.tree.insert(parent, "end", text=item, open=False, values=(abs_path,))
                        # Always add a dummy child to make the folder expandable on click
                        self.tree.insert(node_id, "end", text="loading...")
            except PermissionError:
                pass
            except Exception as e:
                print(f"Error populating tree for {path}: {e}", file=sys.stderr)


        self.tree.delete(*self.tree.get_children())
        # The root node for "ShellOS" (ROOT_DIR)
        root_node = self.tree.insert("", "end", text="ShellOS", open=True, values=(ROOT_DIR,))
        # Populate the immediate children of the root with placeholders
        insert_node(root_node, ROOT_DIR)

        # Add event listener for expanding nodes to dynamically load children
        self.tree.bind("<<TreeviewOpen>>", self.on_tree_open)

    def on_tree_open(self, event):
        """Dynamically loads children when a treeview node is expanded."""
        item = self.tree.focus()
        if not item:
            return

        # Check if the item has a 'loading...' placeholder as its immediate child
        children = self.tree.get_children(item)
        if children and self.tree.item(children[0], "text") == "loading...":
            self.tree.delete(children[0]) # Remove the placeholder

            path_tuple = self.tree.item(item, "values")
            if path_tuple:
                path = path_tuple[0]
                if os.path.isdir(path):
                    try:
                        for sub_item_name in sorted(os.listdir(path)):
                            sub_item_path = os.path.join(path, sub_item_name)
                            # Only load sub-directories if they are within ROOT_DIR
                            if os.path.isdir(sub_item_path) and os.path.abspath(sub_item_path).startswith(ROOT_DIR):
                                sub_node = self.tree.insert(item, "end", text=sub_item_name, open=False, values=(sub_item_path,))
                                # Add a placeholder for further expansion for newly loaded subfolders
                                self.tree.insert(sub_node, "end", text="loading...")
                    except PermissionError:
                        self.tree.insert(item, "end", text="[Permission Denied]", foreground="grey")
                    except Exception as e:
                        self.tree.insert(item, "end", text=f"[Error: {e}]", foreground="red")


    def get_selected_list_items(self):
        """Returns a list of currently selected items in the file listbox."""
        return [self.file_list.get(i) for i in self.file_list.curselection()]

    def load_directory(self, path):
        """Loads and displays the contents of the given directory in the file listbox."""
        # Ensure the path is within the ROOT_DIR before loading
        if not os.path.abspath(path).startswith(ROOT_DIR):
            messagebox.showwarning("Access Denied", "Cannot access directories outside the ShellOS folder.", parent=self)
            # Revert to a safe path if an invalid path was somehow requested
            self.current_path = ROOT_DIR
            path = ROOT_DIR

        self.current_path = path
        self.file_list.delete(0, tk.END)
        try:
            items = os.listdir(path)
            # Separate directories and files, sort them case-insensitively
            dirs = sorted([item for item in items if os.path.isdir(os.path.join(path, item))], key=str.lower)
            files = sorted([item for item in items if os.path.isfile(os.path.join(path, item))], key=str.lower)

            # Insert directories first, then files
            for item in dirs:
                self.file_list.insert(tk.END, item + "/") # Add a slash to denote directories
            for item in files:
                self.file_list.insert(tk.END, item)

        except PermissionError:
            messagebox.showerror("Permission Denied", f"You do not have permission to access:\n{path}", parent=self)
            # Navigate up one level if permission is denied, or revert to previous path
            if self.current_path != ROOT_DIR:
                parent_dir = os.path.dirname(self.current_path)
                self.load_directory(parent_dir)
            else:
                self.file_list.insert(tk.END, "[Permission Denied]") # Indicate failure for root
        except Exception as e:
            messagebox.showerror("Error", f"Could not load directory '{path}':\n{str(e)}", parent=self)

        relative_path = os.path.relpath(path, ROOT_DIR).replace("\\", "/")
        # Update address bar, making it editable temporarily
        self.address_bar.config(state=tk.NORMAL)
        self.address_bar.delete(0, tk.END)
        # Display "ShellOS" instead of "." for the root directory
        display_path = "ShellOS/" + relative_path if relative_path != "." else "ShellOS/"
        self.address_bar.insert(0, display_path)
        self.address_bar.config(state=tk.DISABLED)
        self.update_buttons() # Ensure buttons are updated after loading a new directory

    def on_tree_select(self, event):
        """Handles selection events in the directory treeview."""
        selected_item_id = self.tree.focus()
        if selected_item_id:
            # Retrieve the full path from the item's values
            path_tuple = self.tree.item(selected_item_id, "values")
            if path_tuple:
                path = path_tuple[0]
                # Ensure the selected path is within ROOT_DIR before loading
                if os.path.isdir(path) and os.path.abspath(path).startswith(ROOT_DIR):
                    self.load_directory(path)
            else: # This handles the "ShellOS" root node which might not have a value initially
                if self.tree.item(selected_item_id)['text'] == "ShellOS":
                    self.load_directory(ROOT_DIR)

    def on_listbox_select(self, event):
        """Handles selection events in the file listbox and updates button states."""
        self.update_buttons()

    def update_buttons(self):
        """Updates the state of the action buttons based on listbox selection."""
        has_selection = bool(self.file_list.curselection())

        # Enable/Disable buttons based on selection
        self.rename_btn.config(state=tk.NORMAL if has_selection else tk.DISABLED)
        self.delete_btn.config(state=tk.NORMAL if has_selection else tk.DISABLED)
        self.open_btn.config(state=tk.NORMAL if has_selection else tk.DISABLED)

        # New File and New Folder buttons are always enabled
        self.new_file_btn.config(state=tk.NORMAL)
        self.new_folder_btn.config(state=tk.NORMAL)

    def new_file(self):
        """Prompts user for a new file name and creates an empty file."""
        # Set initialdir to current_path, which is guaranteed to be within ROOT_DIR
        new_path = filedialog.asksaveasfilename(initialdir=self.current_path,
                                                 title="Create New File",
                                                 parent=self)
        if new_path: # if user didn't cancel
            # Ensure the new path is within the ROOT_DIR for security/scope
            if os.path.abspath(new_path).startswith(ROOT_DIR):
                try:
                    with open(new_path, 'w') as f:
                        f.close() # Create empty file
                    self.load_directory(self.current_path) # Reload directory to show new file
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create file: {e}", parent=self)
            else:
                messagebox.showwarning("Access Denied", "Cannot create files outside the ShellOS folder.", parent=self)


    def new_folder(self):
        """Prompts user for a new folder name and creates the folder."""
        # Set initialdir to current_path, which is guaranteed to be within ROOT_DIR
        folder_path = filedialog.askdirectory(initialdir=self.current_path,
                                              title="Create New Folder",
                                              parent=self)
        if folder_path: # if user didn't cancel
            # Ensure the new path is within the ROOT_DIR
            if os.path.abspath(folder_path).startswith(ROOT_DIR):
                try:
                    os.makedirs(folder_path, exist_ok=True) # exist_ok=True prevents error if folder already exists
                    self.load_directory(self.current_path) # Reload directory to show new folder
                    self.populate_tree() # Also refresh the treeview
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create folder: {e}", parent=self)
            else:
                messagebox.showwarning("Access Denied", "Cannot create folders outside the ShellOS folder.", parent=self)


    def rename_item(self):
        """Renames a selected file or folder."""
        selected = self.get_selected_list_items()
        if not selected:
            messagebox.showinfo("Rename", "Please select an item to rename.", parent=self)
            return
        if len(selected) > 1:
            messagebox.showinfo("Rename", "Please select only one item to rename.", parent=self)
            return

        old_name = selected[0]
        # Remove trailing slash if it's a directory for correct path handling
        display_name = old_name.rstrip('/')
        old_full_path = os.path.join(self.current_path, display_name)

        # Prompt for new name
        new_name = tk.simpledialog.askstring("Rename Item", f"Rename '{display_name}' to:",
                                             initialvalue=display_name, parent=self)
        if new_name and new_name != display_name:
            new_full_path = os.path.join(self.current_path, new_name)

            # Security check: ensure operation is within ROOT_DIR
            if not (os.path.abspath(old_full_path).startswith(ROOT_DIR) and os.path.abspath(new_full_path).startswith(ROOT_DIR)):
                messagebox.showwarning("Access Denied", "Operation not allowed outside the ShellOS folder.", parent=self)
                return

            try:
                os.rename(old_full_path, new_full_path)
                self.load_directory(self.current_path)
                self.populate_tree() # Refresh tree in case a folder was renamed
            except FileExistsError:
                messagebox.showerror("Error", f"A file or folder named '{new_name}' already exists.", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename '{display_name}': {e}", parent=self)

    def delete_item(self):
        """Deletes selected files or folders."""
        selected_items = self.get_selected_list_items()
        if not selected_items:
            messagebox.showinfo("Delete", "Please select item(s) to delete.", parent=self)
            return

        confirm_msg = f"Are you sure you want to delete the following item(s) permanently?\n\n" + "\n".join(selected_items)
        if not messagebox.askyesno("Confirm Delete", confirm_msg, icon='warning', parent=self):
            return # User canceled

        deleted_any = False
        for item_name in selected_items:
            # Remove trailing slash for path calculation if it's a directory
            actual_item_name = item_name.rstrip('/')
            full_path = os.path.join(self.current_path, actual_item_name)

            # Security check: ensure operation is within ROOT_DIR
            if not os.path.abspath(full_path).startswith(ROOT_DIR):
                messagebox.showwarning("Access Denied", f"Cannot delete '{item_name}' outside the ShellOS folder.", parent=self)
                continue

            try:
                if os.path.isdir(full_path):
                    # Use shutil.rmtree for non-empty directories if needed,
                    # but os.rmdir is safer as it only deletes empty ones.
                    # For a simple file manager, requiring empty dir is fine.
                    os.rmdir(full_path)
                else:
                    os.remove(full_path)
                deleted_any = True
            except OSError as e:
                messagebox.showerror("Error Deleting", f"Could not delete '{item_name}':\n{e}", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred while deleting '{item_name}': {e}", parent=self)

        if deleted_any:
            self.load_directory(self.current_path)
            self.populate_tree() # Refresh tree as folders might have been deleted

    def open_item(self):
        """Opens selected files or navigates into selected folders."""
        selected = self.file_list.curselection() # Get currently selected indices
        if not selected:
            messagebox.showinfo("Open", "Please select an item to open.", parent=self)
            return

        # Always take the first selected item for opening in this context
        item_name = self.file_list.get(selected[0])
        # Remove trailing slash if it's a directory
        actual_item_name = item_name.rstrip('/')
        path = os.path.join(self.current_path, actual_item_name)
        self.try_open(path)

    def on_double_click(self, event):
        """Handles double-click events in the file listbox."""
        # Find the element closest to the click coordinates
        index = self.file_list.nearest(event.y)
        if index is not None and index < self.file_list.size():
            # Set the selection to the clicked item
            self.file_list.selection_clear(0, tk.END)
            self.file_list.selection_set(index)
            self.file_list.activate(index)
            self.update_buttons() # Update buttons based on the new selection

            name = self.file_list.get(index)
            # Remove trailing slash if it's a directory
            actual_name = name.rstrip('/')
            path = os.path.join(self.current_path, actual_name)
            self.try_open(path)

    def try_open(self, path):
        """Attempts to open a file or navigate to a directory."""
        # Security check: ensure operation is within ROOT_DIR
        if not os.path.abspath(path).startswith(ROOT_DIR):
            messagebox.showwarning("Access Denied", "Cannot open items outside the ShellOS folder.", parent=self)
            return

        try:
            if os.path.isdir(path):
                self.load_directory(path)
            elif os.path.isfile(path):
                if path.endswith(".txt"):
                    # Assuming notepad.py exists and handles the file opening
                    # This requires 'notepad.py' to be in 'System64/programs/'
                    notepad_script_path = os.path.join(ROOT_DIR, "System64", "programs", "notepad.py")
                    if os.path.exists(notepad_script_path):
                        subprocess.Popen([sys.executable, notepad_script_path, path])
                    else:
                        messagebox.showerror("Error", "notepad.py not found at expected path.", parent=self)
                else:
                    # Use os.startfile for Windows, equivalent for other OS is os.xdg-open or subprocess.call(['open', path])
                    # platform.system() can be used to differentiate
                    if platform.system() == "Windows":
                        os.startfile(path)
                    elif platform.system() == "Darwin": # macOS
                        subprocess.call(['open', path])
                    else: # Linux and others
                        subprocess.call(['xdg-open', path])
        except PermissionError:
            messagebox.showerror("Permission Denied", f"You do not have permission to open:\n{path}", parent=self)
        except FileNotFoundError:
            messagebox.showerror("Not Found", f"The item '{os.path.basename(path)}' was not found.", parent=self)
        except Exception as e:
            messagebox.showerror("Error Opening Item", f"Could not open '{os.path.basename(path)}':\n{e}", parent=self)


if __name__ == "__main__":
    app = ShellOSFileManager()
    app.mainloop()