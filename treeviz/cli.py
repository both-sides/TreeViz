import argparse
import sys

from .config import DEFAULTS
from .walker import walk

def main():
    parser = argparse.ArgumentParser(prog = "treeviz", description = "helps visualize file tree structure, and also provides TUI file explorer")
    parser.add_argument("path", nargs = "?", default = ".")
    parser.add_argument("--max-depth", type = int, default = DEFAULTS["max_depth"], help="Maximum recursion depth (root = 0).")
    parser.add_argument("--json", action = "store_true")
    parser.add_argument("--max-entries", type=int, default=DEFAULTS["max_entries_per_node"], help="Max entries to show per directory; remaining are truncated.")
    parser.add_argument("--follow-symlinks", action="store_true", help="If set, will follow symlinks to directories (with cycle detection).")


    #TODO: add flags for other formats

    args = parser.parse_args()

    #TODO: route to correct formatter or TUI
    for node in walk(
            root = args.path, 
            max_depth = args.max_depth,
            max_entries_per_node = args.max_entries,
            follow_symlinks = args.follow_symlinks
            ):

        _print_node(node)

def _print_node(node, prefix=""):
    """
    Simple recursive printing for debugging:
      prefix ├── node.name
             └── child.name
    (ASCII style; no fancy box-drawing yet).
    """
    print(prefix + node.name)
    for i, child in enumerate(node.children):
        is_last = (i == len(node.children) - 1)
        branch = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")
        print(prefix + branch + child.name)
        # Recurse further if this child has children
        if child.children:
            _print_subtree(child, child_prefix)

def _print_subtree(node, prefix):
    """Helper to recursively print an entire subtree under `node` from CLI."""
    for i, child in enumerate(node.children):
        is_last = (i == len(node.children) - 1)
        branch = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")
        print(prefix + branch + child.name)
        if child.children:
            _print_subtree(child, child_prefix)

