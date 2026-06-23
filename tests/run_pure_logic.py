#!/usr/bin/env python3
"""Run SpectorCore test harness: headless execution + static audit fallback."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXEC = ROOT / "tests" / "execute_core_tests.py"


def main():
    proc = subprocess.run([sys.executable, str(EXEC)], capture_output=False)
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()