# 🌳 TreeViz (WIP) 
**Fast & Interactive Visualization for Large Hierarchies**

> **Status:** 🚧 Work in Progress — traversal, metrics, and CLI packaging implemented.  
> Visualization (Graphviz/NetworkX/TUI) under active development.

TreeViz is a Python-based tool for exploring massive hierarchical or graph structures.  
It combines efficient recursive directory traversal with flexible visualizations (Graphviz, NetworkX, or text-based TUIs) to make sense of data at any scale.

---

## 🚀 Features
- **Robust traversal engine**
  - Recursive filesystem walking with symlink awareness
  - Graceful handling of permission errors, broken links, and unreadable directories
  - Truncation markers when directories exceed max entries
- **Metrics & summaries**
  - Automatic counters for files vs directories
  - Future support for size, timestamps, and custom metadata
- **CLI interface**
  - `treeviz <path>` with flags for depth, max entries, symlink following, etc.
  - Installs as a command-line tool via `setup.py`
- **Visualization backends** (WIP)
  - Graphviz / DOT export
  - NetworkX graph analysis
  - Rich / Textual TUI for interactive exploration
  - Planned: Tkinter / PyQt GUI
- **Cross-platform support**
  - Tested on Linux, macOS, WSL; Windows support in progress

---

## 📸 Demo
<img width="494" height="617" alt="image" src="https://github.com/user-attachments/assets/4fcb0697-a625-4199-92b1-3bc559c5dda7" />

with --tui cli flag 
<img width="739" height="1007" alt="image" src="https://github.com/user-attachments/assets/e118b025-7c63-48e6-948f-1ea005ceba97" />




---

## 🛠️ Tech Stack
- **Core:** Python 3.9+
- **Visualization:** Graphviz, NetworkX, Rich/Textual, Tkinter/PyQt (planned)
- **Packaging:** setuptools (`setup.py` entrypoint)

---

## 📦 Installation
```bash
git clone https://github.com/both-sides/TreeViz.git
cd TreeViz

#recommended (but optional if your distribution allows global pip installation): create a python virtual enviroment
    python -m venv .venv
    source .venv/bin/activate

pip install -r requirements/requirements.txt

# optional:
    pip install -r requirements/requirements-tui.txt
    pip install -r requirements/requirements-gui.txt
    pip install -r requirements/requirements-legacy.txt
    pip install -r requirements/requirements-dev.txt

pip install -e .

```

## 🔧 Usage
```bash

# Traverse and print a directory tree
treeviz ~/ --max-entries 50

# Follow symlinks and show summary counts
treeviz /etc --follow-symlinks

# Launch the interactive TUI (work in progress)
treeviz ~/ --tui
```

## 📍 Roadmap
- [x] Safe recursive traversal (with error handling)  
- [x] CLI parser + entrypoint  
- [x] Directory/file summary counters  
- [ ] Rich TUI for interactive browsing  
- [ ] Graphviz & NetworkX visualizers  
- [ ] GUI frontend (Tkinter/PyQt)  
- [ ] Plugin system for custom metrics  


