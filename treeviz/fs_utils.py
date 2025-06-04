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


