import os
from .model import Node
#from .config import DEFAULTS

def walk(root_path, max_depth = 5, follow_symlinks = False):
    #TODO: implement recursive scan with cycle detection
    yield Node(name = os.path.basename(root_path), path = root_path)
