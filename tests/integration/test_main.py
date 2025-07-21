import subprocess
import sys


def test_main_entrypoint_runs_without_error(tmp_path):
    # exécute ton module comme un script
    result = subprocess.run(
        [sys.executable, "-m", "trading_framework"],
        cwd=tmp_path,
        capture_output=True,
    )
    assert result.returncode == 0
