#A simple tree node representing a single file or directory



class Node:
    def __init__(self, name, path, children = None):
        self.name = name #basename (string)
        self.path = path #full path to this node (string)
        self.children = children or [] #list of child node objects (will be populated by walker)
        self.expanded = False # reserved for TUI

    def __repr__(self):
        return f"<Node {self.path!r}>"
