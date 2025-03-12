import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys


class JSONTreeViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Collapsible JSON Viewer")
        self.geometry("800x600")

        # Create a menu
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open JSON", command=self.open_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)

        # Create a Treeview
        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill="both")

    def open_json(self, file_path=None):
        # If no file path was passed, prompt the user to choose a file
        if not file_path:
            file_path = filedialog.askopenfilename(
                title="Open JSON File",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
            )
        if not file_path:
            return

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            messagebox.showerror("Error", f"Failed to load JSON:\n{e}")
            return

        # Clear the tree first
        self.tree.delete(*self.tree.get_children())
        self.title(f"Collapsible JSON Viewer - {file_path}")

        # Insert the JSON data into the tree
        self.insert_json("", "root", data)

        # By default, expand the root item
        root_children = self.tree.get_children("")
        if root_children:
            self.tree.item(root_children[0], open=True)

    def insert_json(self, parent, key, value):
        """
        Recursively insert JSON data into the Treeview.
        parent: parent node in the tree
        key: dictionary key or list index
        value: the data to insert
        """
        # Display the key in the tree label
        if isinstance(value, dict):
            # Show the node label as 'key: { ... }'
            node_id = self.tree.insert(parent, "end", text=f"{key}: {{}}")
            # Recursively insert each item in the dict
            for subkey, subval in value.items():
                self.insert_json(node_id, subkey, subval)
        elif isinstance(value, list):
            # Show the node label as 'key: [ ... ]'
            node_id = self.tree.insert(parent, "end", text=f"{key}: []")
            # Recursively insert each index in the list
            for i, item in enumerate(value):
                self.insert_json(node_id, f"[{i}]", item)
        else:
            # It's a primitive (str, int, float, bool, None)
            # Show the node label as 'key: value'
            display_text = f"{key}: {value!r}"
            self.tree.insert(parent, "end", text=display_text)


def main():
    app = JSONTreeViewer()

    # If a file path is passed in (e.g., by double-clicking a file associated with this exe),
    # try to open it immediately.
    if len(sys.argv) > 1:
        file_to_open = sys.argv[1]
        if os.path.isfile(file_to_open):
            app.open_json(file_to_open)

    app.mainloop()


if __name__ == "__main__":
    main()