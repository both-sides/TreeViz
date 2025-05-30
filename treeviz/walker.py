import os
from .model import Node
from .config import DEFAULTS

def walk(root_path, max_depth = DEFAULTS[max_depth], follow_symlinks = False):
    
