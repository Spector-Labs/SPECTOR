#!/usr/bin/env python3
"""Run full verification plan and write git + scratch evidence."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = Path(r"C:\Users\USER\AppData\Local\Temp\grok-goal-ee54e3f7c3b7\implementer")
SCRATCH.mkdir(parents=True, exist_ok=True)


def run(label, script):
    print(f"\n{'='*60}\n{label}\n{'='*60}")
    proc = subprocess.run([sys.executable, str(script)], cwd=str(ROOT))
    return proc.returncode


def capture_git_evidence():
    out = SCRATCH / "git-evidence.txt"
    cmds = [
        ["git", "-C", str(ROOT), "log", "-5", "--oneline"],
        ["git", "-C", str(ROOT), "status", "--short"],
        ["git", "-C", str(ROOT), "ls-files"],
    ]
    lines = ["=== GIT EVIDENCE ===", f"repo: {ROOT}", ""]
    for cmd in cmds:
        lines.append(f"$ {' '.join(cmd)}")
        proc = subprocess.run(cmd, capture_output=True, text=True)
        lines.append(proc.stdout or "")
        if proc.stderr:
            lines.append(proc.stderr)
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


def main():
    steps = [
        ("verify_static.py", ROOT / "tests" / "verify_static.py"),
        ("execute_core_tests.py", ROOT / "tests" / "execute_core_tests.py"),
        ("verify_offline_sw.py", ROOT / "tests" / "verify_offline_sw.py"),
        ("capture_launch.py", ROOT / "tests" / "capture_launch.py"),
        ("write_scratch_evidence.py", ROOT / "tests" / "write_scratch_evidence.py"),
    ]
    failed = []
    for name, path in steps:
        if run(name, path) != 0:
            failed.append(name)

    capture_git_evidence()

    if failed:
        print("FAILED:", failed)
        sys.exit(1)
    print("ALL VERIFICATION STEPS PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()