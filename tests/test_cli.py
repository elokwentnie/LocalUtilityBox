"""Smoke tests for the master CLI entry point."""
import subprocess
import sys


def test_localutilitybox_runs():
    result = subprocess.run(
        [sys.executable, "-m", "cli"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "LocalUtilityBox" in result.stdout
    assert "Image Processing" in result.stdout
    assert "PDF Operations" in result.stdout
    assert "Video / Audio" in result.stdout
