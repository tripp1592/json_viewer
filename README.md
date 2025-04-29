# JSON Viewer

A lightweight, cross-platform GUI application to view and explore JSON and JSONC (JSON with comments) files.

## Features

- **JSON & JSONC support**: Load standard JSON or JSONC files with `//…` and `/*…*/` comments, trailing commas, and more—all parsed via [`json5`](https://pypi.org/project/json5/).
- **Tree‑structure view**: Browse nested objects and arrays in an expandable/collapsible tree.
- **Details popup**: Double‑click any value to open a resizable popup showing the full text.
- **Command‑line & dialog loading**: Open a file at startup by passing its path as an argument, or click **Load JSON** to choose via file dialog.
- **Collapse all**: Quickly collapse all nodes with the **Collapse All** button.

## Installation

1. **Clone or download** this repository.
2. **Install dependencies** (requires Python 3.7+):

   ```bash
   pip install json5
   ```

## Usage

From the project root:

```bash
# Run the viewer on a file immediately:
python main.py path/to/data.jsonc

# Or start it blank and load via the button
python main.py
```

- File‑dialog filters for `*.json;*.jsonc` by default.
- Double‑click any node value to see a full‑text popup.

## Packaging with PyInstaller

To bundle into a standalone Windows executable:

```bash
pyinstaller \
  --name JSONViewer \
  --onefile \
  --windowed \
  --hidden-import=json5 \
  main.py
```

- `--onefile` packs everything into a single `.exe`.
- `--windowed` suppresses the console window on launch.
- `--hidden-import=json5` ensures the `json5` module is bundled.

After building, the executable will support JSONC files out of the box.

## Troubleshooting

- **Invalid escape errors**: Ensure string values use valid escapes (e.g., `\\` for a backslash). If you must support raw backslashes, consider adjusting the loader to auto‑escape them before parsing.
- **UI issues on macOS/Linux**: You may need to install system‐specific Tkinter packages (e.g., `sudo apt install python3-tk` on Debian/Ubuntu).

## License

[MIT License](LICENSE)

