class Node:
    def __init__(self, name, path, children = None):
        self.name = name
        self.path = path
        self.children = children or []
        self.expanded = False

    def __repr__(self):
        return f"<Node {self.path!r}>"
