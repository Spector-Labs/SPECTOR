#!/usr/bin/env python3
"""Deprecated — use tests/run_verification.py as the single entry point."""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    script = Path(__file__).resolve().parent / "run_verification.py"
    sys.exit(subprocess.call([sys.executable, str(script)]))