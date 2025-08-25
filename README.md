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
*(In progress — CLI output + Graphviz screenshots coming soon)*

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
pip install -r requirements/requirements.txt
# optional:
    pip install -r requirements/requirements-tui.txt
    pip install -r requirements/requirements-gui.txt
    pip install -r requirements/requirements-legacy.txt
    pip install -r requirements/requirements-dev.txt
pip install -e .



pip install -e .
```

## 🔧 Usage
```bash

# Traverse and print a directory tree
treeviz ~/projects --depth 2 --max-entries 50

# Follow symlinks and show summary counts
treeviz /etc --follow-symlinks --summary

# Launch the interactive TUI (work in progress)
treeviz ~/projects --tui
```

## 📍 Roadmap
- [x] Safe recursive traversal (with error handling)  
- [x] CLI parser + entrypoint  
- [x] Directory/file summary counters  
- [ ] Rich TUI for interactive browsing  
- [ ] Graphviz & NetworkX visualizers  
- [ ] GUI frontend (Tkinter/PyQt)  
- [ ] Plugin system for custom metrics  


