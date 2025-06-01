import subprocess
import sys

def test_cli_basic(tmp_path):
    #stub test to ensure CLI runs without crashing
    result = subprocess.run([sys.executable, "-m", "treeviz.cli", str(tmp_path)], capture_output = True)
    assert result.returncode == 0
