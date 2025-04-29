import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import json5

# Global variable to track the details popup window
detail_popup = None


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
    Load JSON (with comments) from a file. If file_path is not provided, prompt the user.
    Without a dummy root, top-level items are added directly and collapsed by default.
    """
    if not file_path:
        file_path = filedialog.askopenfilename(
            title="Open JSON File",
            filetypes=[("JSON Files", "*.json;*.jsonc"), ("All Files", "*.*")],
        )
    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json5.load(f)
        # Clear any existing items
        for child in tree.get_children():
            tree.delete(child)

        # Insert top-level data
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    node = tree.insert(
                        "", "end", text=str(key), values=[""], open=False
                    )
                    build_tree(tree, node, value)
                else:
                    tree.insert("", "end", text=str(key), values=[repr(value)])
        elif isinstance(data, list):
            for i, value in enumerate(data):
                if isinstance(value, (dict, list)):
                    node = tree.insert(
                        "", "end", text=f"[{i}]", values=[""], open=False
                    )
                    build_tree(tree, node, value)
                else:
                    tree.insert("", "end", text=f"[{i}]", values=[repr(value)])
        else:
            tree.insert("", "end", text=repr(data), values=[""])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON:\n{e}")


def collapse_all(tree, node=""):
    """
    Recursively collapse all nodes in the Treeview.
    """
    if node == "":
        for child in tree.get_children():
            collapse_all(tree, child)
    else:
        tree.item(node, open=False)
        for child in tree.get_children(node):
            collapse_all(tree, child)


def show_popup(text):
    """
    Create (or update) a pop-up window to display full text with wrapping.
    Only one details window is allowed at a time.
    """
    global detail_popup
    if detail_popup is not None and detail_popup.winfo_exists():
        text_widget = detail_popup.text_widget
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        detail_popup.lift()
        return

    detail_popup = tk.Toplevel()
    detail_popup.title("Details")
    detail_popup.geometry("600x400")

    text_widget = tk.Text(detail_popup, wrap="word")
    text_widget.insert("1.0", text)
    text_widget.config(state="disabled")
    text_widget.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(detail_popup, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    detail_popup.text_widget = text_widget

    def on_destroy(event):
        global detail_popup
        detail_popup = None

    detail_popup.bind("<Destroy>", on_destroy)


def on_item_double_click(event, tree):
    """
    Handle double-click events on the Treeview.
    """
    region = tree.identify("region", event.x, event.y)
    if region == "icon":
        return

    item_id = tree.identify_row(event.y)
    if not item_id:
        return
    key_text = tree.item(item_id, "text")
    values = tree.item(item_id, "values")
    value_text = values[0] if values else ""

    if not value_text.strip():
        return

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

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    btn_load = ttk.Button(
        button_frame, text="Load JSON", command=lambda: load_json(tree)
    )
    btn_load.pack(side="left", padx=5)

    btn_collapse = ttk.Button(
        button_frame, text="Collapse All", command=lambda: collapse_all(tree)
    )
    btn_collapse.pack(side="left", padx=5)

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        load_json(tree, file_path)

    root.mainloop()


if __name__ == "__main__":
    main()
