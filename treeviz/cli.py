import argparse

from .config import DEFAULTS
from .walker import walk

def main():
    parser = argparse.ArgumentParser(prog = "treeviz", description = "helps visualize file tree structure, and also provides TUI file explorer")
    parser.add_argument("path", nargs = "?", default = ".")
    parser.add_argument("--max-depth", type = int, default = DEFAULTS["max_depth"])
    parser.add_argument("--json", action = "store_true")
    #TODO: add flags for other formats
    args = parser.parse_args()

    #TODO: route to correct formatter or TUI
    for node in walk(args.path, max_depth = args.max_depth):
        print(node)

