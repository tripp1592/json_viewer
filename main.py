import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import sys


def build_tree(tree, parent, data):
    """
    Recursively insert JSON data into the Treeview.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                node = tree.insert(parent, "end", text=str(key), values=[""])
                build_tree(tree, node, value)
            else:
                tree.insert(parent, "end", text=str(key), values=[repr(value)])
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                node = tree.insert(parent, "end", text=f"[{index}]", values=[""])
                build_tree(tree, node, item)
            else:
                tree.insert(parent, "end", text=f"[{index}]", values=[repr(item)])
    else:
        tree.insert(parent, "end", text=repr(data), values=[""])


def load_json(tree, file_path=None):
    """
    Load JSON from a file. If file_path is not provided,
    prompt the user with a file dialog.
    """
    if not file_path:
        file_path = filedialog.askopenfilename(
            title="Open JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Clear existing tree items
        for child in tree.get_children():
            tree.delete(child)
        # Insert a root node and build the tree
        root_node = tree.insert("", "end", text="root", values=[""], open=True)
        build_tree(tree, root_node, data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON:\n{e}")


def show_popup(text):
    """
    Create a pop-up window to display the full text with wrapping.
    """
    popup = tk.Toplevel()
    popup.title("Details")
    popup.geometry("600x400")

    text_widget = tk.Text(popup, wrap="word")
    text_widget.insert("1.0", text)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(popup, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")


def on_item_double_click(event, tree):
    """
    On double-click, show a pop-up with the full key and value.
    """
    item_id = tree.identify_row(event.y)
    if not item_id:
        return
    key_text = tree.item(item_id, "text")
    values = tree.item(item_id, "values")
    value_text = values[0] if values else ""
    full_text = f"Key: {key_text}\nValue: {value_text}"
    show_popup(full_text)


def main():
    root = tk.Tk()
    root.title("JSON Viewer")
    root.geometry("800x600")

    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    vsb = ttk.Scrollbar(frame, orient="vertical")
    vsb.grid(row=0, column=1, sticky="ns")

    hsb = ttk.Scrollbar(frame, orient="horizontal")
    hsb.grid(row=1, column=0, sticky="ew")

    tree = ttk.Treeview(
        frame,
        columns=["Value"],
        show="tree headings",
        yscrollcommand=vsb.set,
        xscrollcommand=hsb.set,
    )
    tree.heading("#0", text="Key")
    tree.heading("Value", text="Value")
    tree.column("#0", width=300, minwidth=150)
    tree.column("Value", width=500, minwidth=150)
    tree.grid(row=0, column=0, sticky="nsew")

    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    tree.bind("<Double-1>", lambda event: on_item_double_click(event, tree))

    btn_load = ttk.Button(root, text="Load JSON", command=lambda: load_json(tree))
    btn_load.pack(pady=10)

    # If a JSON file is passed as a command-line argument, load it automatically.
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        load_json(tree, file_path)

    root.mainloop()


if __name__ == "__main__":
    main()
