# debug_walk.py
from treeviz.walker import walk
import sys

if len(sys.argv) < 2:
    print("Usage: python debug_walk.py <path>")
    sys.exit(1)

root = sys.argv[1]
nodes = list(walk(root, max_depth=2, max_entries_per_node=50, follow_symlinks=False))

# Print a very basic view of the returned Node(s)
def dump(node, indent=0):
    print(" " * (indent*2) + "- " + node.name)
    for child in node.children:
        dump(child, indent + 1)

for n in nodes:
    dump(n)

