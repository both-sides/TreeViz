import pytest
import treeviz.walker
from treeviz.walker import walk

def test_walk_empty(tmp_path):
    root = tmp_path / "empty"
    root.mkdir()
    nodes = list(walk(str(root))) #forces walk generator to run till completion
    assert len(nodes) >= 1, "there should be at least one node"
