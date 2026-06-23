#!/usr/bin/env python3
"""Capture python -m http.server stdout/stderr for verification evidence."""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
SCRATCH = Path(r"C:\Users\USER\AppData\Local\Temp\grok-goal-ee54e3f7c3b7\implementer")
SCRATCH.mkdir(parents=True, exist_ok=True)


def run_once(label, log_path):
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8088", "--directory", str(PUBLIC)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    lines = [f"=== {label} ===", f"command: python -m http.server 8088 --directory {PUBLIC}", ""]
    time.sleep(2)

    for path in ["index.html", "app.html", "style.css", "manifest.json", "app.html?script=dGVzdA=="]:
        url = f"http://127.0.0.1:8088/{path}"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                lines.append(f"GET /{path} -> {resp.status} ({len(resp.read())} bytes)")
        except Exception as e:
            lines.append(f"GET /{path} -> ERROR: {e}")

    time.sleep(8)
    proc.terminate()
    try:
        out, _ = proc.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, _ = proc.communicate()
    lines.append("")
    lines.append("=== server stdout/stderr (~10s) ===")
    lines.append(out or "(no output)")
    log_path.write_text("\n".join(lines), encoding="utf-8")
    return lines


def main():
    log1 = SCRATCH / "launch-1.log"
    log2 = SCRATCH / "launch-2.log"
    combined = SCRATCH / "launch.log"

    r1 = run_once("RUN 1", log1)
    time.sleep(1)
    r2 = run_once("RUN 2", log2)

    combined.write_text("\n".join(r1 + ["", ""] + r2), encoding="utf-8")
    print(combined.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()