# treeviz/walker.py

import os
import sys
import stat

from .model import Node
from .config import DEFAULTS
from .fs_utils import safe_scandir, is_dir, UnreadableDirectory

def walk(root_path, max_depth=DEFAULTS["max_depth"], max_entries_per_node=100, follow_symlinks=False):
    """
    Perform a depth‐first traversal of the filesystem, starting at root_path.
    Yields Node instances (with children lists) for each directory‐or‐file.

    - max_depth (int): maximum recursion depth (root is depth=0).
    - max_entries_per_node (int): if a directory has more entries than this,
      only the first `max_entries_per_node` are included; a '... (n more)' marker
      Node is appended to indicate truncation.
    - follow_symlinks (bool): if True, follow symbolic links to directories 
      (while still detecting cycles).

    Cycle detection: we keep a set of visited inodes (st_dev, st_ino). Once we
    see a directory whose inode (and device) matches something we've visited,
    we do **not** descend into it again.
    """
    # Normalize to an absolute path
    root_abs = os.path.abspath(root_path)

    # Keep track of (st_dev, st_ino) for every directory we visit,
    # so we can detect symlink‐loops and hard‐link loops.
    visited_inodes = set()

    def _walk(path, depth):
        """
        Internal recursive generator. Yields a fully‐built Node for this path,
        with its children attached (or, if permission denied, a marker).
        """
        # Try to stat the path, catching the possibility that it's broken or unreadable
        try:
            stat_info = os.stat(path, follow_symlinks=follow_symlinks)
        except (PermissionError, FileNotFoundError, OSError):
            # Permission denied or file not found: produce a single “unreadable” node
            # or skip entirely. Here, we'll yield a node named “[unreadable]”.
            name = os.path.basename(path) or path
            unreadable = Node(name=f"[unreadable: {name}]", path=path, children=[])
            return [unreadable]

        # If it's not a directory (or if depth >= max_depth), just yield a file node
        if not stat.S_ISDIR(stat_info.st_mode) or depth >= max_depth:
            name = os.path.basename(path) or path
            return [Node(name=name, path=path, children=[])]

        # At this point, it’s a directory and we have room to descend
        # Check for cycles: use (device, inode)
        inode_key = (stat_info.st_dev, stat_info.st_ino)
        if inode_key in visited_inodes:
            # Already visited; produce a cycle‐marker node instead of descending
            name = os.path.basename(path) or path
            cycle_node = Node(name=f"[cycle: {name}]", path=path, children=[])
            return [cycle_node]

        # Mark this directory as visited
        visited_inodes.add(inode_key)

        # Create a node for this directory; we’ll append children next
        dir_name = os.path.basename(path) or path
        this_node = Node(name=dir_name, path=path, children=[])

        # Attempt to list directory entries
        entries = []
        try:
            for entry in safe_scandir(path):
                entries.append(entry)
        except UnreadableDirectory:
            # Replace with a single “unreadable” node
            unreadable = Node(name=f"[unreadable: {dir_name}]", path=path, children=[])
            return [unreadable]

        # Sort entries alphabetically (folders first, then files)
        entries.sort(key=lambda e: (not is_dir(e, follow_symlinks), e.name.lower()))

        # Truncate to max_entries_per_node if necessary
        truncated = False
        if len(entries) > max_entries_per_node:
            truncated = True
            entries = entries[:max_entries_per_node]

        # Recurse into each entry
        for entry in entries:
            child_path = entry.path
            # If it’s a directory (honoring follow_symlinks), recurse; otherwise, file node
            if is_dir(entry, follow_symlinks=follow_symlinks):
                child_nodes = _walk(child_path, depth + 1)
                for cn in child_nodes:
                    this_node.children.append(cn)
            else:
                # File (or broken symlink to a file)
                this_node.children.append(Node(name=entry.name, path=child_path, children=[]))

        # If truncated, add a marker node at the end indicating N more entries
        if truncated:
            remaining = len(os.listdir(path)) - max_entries_per_node
            marker = Node(name=f"[… {remaining} more entries]", path=path, children=[])
            this_node.children.append(marker)

        return [this_node]

    # Kick off recursion at depth=0
    top_nodes = _walk(root_abs, depth=0)
    for node in top_nodes:
        yield node

