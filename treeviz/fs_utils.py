#I'm trying to catch permission errors or file not found when trying to list a directory.

import os 
#import stat

class UnreadableDirectory(Exception): #Signal that a directory cannot be read (e.g. permission denied).
    pass 


def safe_scandir(path):
    try:
        with os.scandir(path) as it: #should close the resource(ScandirIterator) if errors are caught
            for entry in it:
                yield entry
    except(PermissionError, FileNotFoundError, OSError) as e:
        raise UnreadableDirectory(str(e)) # should wrap this custom exception so that walker can catch it


def is_dir(entry, follow_symlinks): # should return true if entry is a directory , and should honor symlink flag
    try:
        return entry.is_dir(follow_symlinks = follow_symlinks) #.is_dir here is a method from os.DirEntry object, not a recursive call
    except OSError:
        return False #if the stat fails treat as non-dir

def count_nodes(node):
    files = 0 
    dirs = 0
    stack = [node]
    while stack:
        current = stack.pop()
        if current.children:
            dirs += 1
            stack.extend(current.children)
        else:
            files += 1
    return files, dirs

def list_children(
        path: str,
        follow_symlinks: bool,
        max_entries: int | None = None,
):
    """
    Returns (dirs, files, truncated_count). Each element is (name, full_path, is_directory).
    """
    try:
        entries = list(safe_scandir(path))
    except Exception:
        raise UnreadableDirectory(f"Cannot read directory: {path}")
    
    # Directories first, alphabetical
    entries.sort(key=lambda e: (not is_dir(e, follow_symlinks), e.name.lower()))

    total = len(entries)
    if max_entries is not None and total > max_entries:
        entries = entries[:max_entries]
        truncated = total - max_entries
    else:
        truncated = 0

    out = []
    for e in entries:
        full_path = e.path  # already absolute from scandir(parent)
        out.append((e.name, full_path, is_dir(e, follow_symlinks)))

    return out, truncated