from __future__ import annotations
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, Static
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.message import Message
import os
from treeviz.fs_utils import list_children, UnreadableDirectory

class TreeVizApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    #main {
        height: 1fr;
    }
    #sidebar {
        width: 40%;
        padding: 1 2;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("e", "expand_all", "Expand subtree"),
        ("c", "collapse_all", "Collapse subtree"),
    ]

    root_path: str
    follow_symlinks: bool
    max_entries: int | None

    dirs_count = reactive(0)
    files_count = reactive(0)

    class NodeOpened(Message):
        def __init__(self, path: str) -> None:
            self.path = path
            super().__init__()

    def __init__(self, root_path: str, follow_symlinks: bool, max_entries: int | None):
        super().__init__()
        self.root_path = os.path.abspath(root_path)
        self.follow_symlinks = follow_symlinks
        self.max_entries = max_entries

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            self.fs_tree = Tree(self.root_path, id="tree")
            self.info = Static("", id="sidebar")
            yield self.fs_tree
            yield self.info
        yield Footer()

    def on_mount(self) -> None:
        # lazy root load: add a placeholder child so it shows as expandable
        root_node = self.fs_tree.root
        root_node.allow_expand = True
        self._update_status()

    def _update_status(self, extra: str = ""):
        summary = f"[bold]Dirs:[/bold] {self.dirs_count}   [bold]Files:[/bold] {self.files_count}"
        self.info.update(summary + (f"\n{extra}" if extra else ""))

    async def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node = event.node
        if node.children:  # already loaded
            return
        path = self._path_of(node)
        await self._populate(node, path)

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        # Update sidebar with info
        path = self._path_of(event.node)
        try:
            s = os.stat(path, follow_symlinks=self.follow_symlinks)
            kind = "Dir" if os.path.isdir(path) else "File"
            self._update_status(f"[bold]{kind}[/bold]\n{path}\nsize={s.st_size} bytes")
        except Exception:
            self._update_status(f"[bold]Unknown[/bold]\n{path}")

    def _path_of(self, node: Tree.Node) -> str:
        # Reconstruct the path from labels (root label is absolute already)
        labels = []
        cur = node
        while cur and cur is not self.fs_tree.root:
            labels.append(str(cur.label))
            cur = cur.parent
        labels.reverse()
        return os.path.join(self.root_path, *labels) if labels else self.root_path

    async def _populate(self, node: Tree.Node, path: str) -> None:
        try:
            items, truncated = list_children(path, self.follow_symlinks, self.max_entries)
        except UnreadableDirectory:
            node.add("[unreadable]")
            return

        # Add children: directories first already ensured
        for name, full, is_dir in items:
            child = node.add(name)
            if is_dir:
                child.allow_expand = True
                self.dirs_count += 1
            else:
                self.files_count += 1

        if truncated:
            node.add(f"[… {truncated} more entries]")

        node.expand()
        self._update_status()

    async def action_refresh(self) -> None:
        # reload currently selected node
        node = self.fs_tree.cursor_node or self.fs_tree.root
        node.remove_children()
        if node is self.fs_tree.root:
            self.dirs_count = 0
            self.files_count = 0
        await self._populate(node, self._path_of(node))

    async def action_expand_all(self) -> None:
        # cautious: breadth-first expand from current node, with max 200 nodes to avoid explosions
        limit = 200
        queue = [self.fs_tree.cursor_node or self.fs_tree.root]
        seen = 0
        while queue and seen < limit:
            n = queue.pop(0)
            if not n.children:
                await self._populate(n, self._path_of(n))
            n.expand()
            queue.extend(list(n.children))
            seen += 1

    async def action_collapse_all(self) -> None:
        node = self.fs_tree.cursor_node or self.fs_tree.root
        # keep node but collapse all descendants
        for desc in list(node.children):
            desc.collapse()
        node.collapse()

def run_tui(root_path: str, follow_symlinks: bool, max_entries: int | None):
    app = TreeVizApp(
        root_path=root_path,
        follow_symlinks=follow_symlinks,
        max_entries=max_entries,
    )
    app.run()   # no kwargs here