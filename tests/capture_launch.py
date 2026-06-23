#!/usr/bin/env python3
"""Capture python -m http.server stdout/stderr for two ~5s background runs."""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
SCRATCH = Path(r"C:\Users\USER\AppData\Local\Temp\grok-goal-ee54e3f7c3b7\implementer")
SCRATCH.mkdir(parents=True, exist_ok=True)
PORT = 8088


def capture_server_transcript(label, log_path, seconds=5):
    cmd = [sys.executable, "-m", "http.server", str(PORT), "--directory", str(PUBLIC)]
    header = [
        f"=== {label} ===",
        f"command: {' '.join(cmd)}",
        f"background duration: {seconds}s (request sent at +1s)",
        "",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    time.sleep(1)
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/index.html", timeout=3)
    except Exception:
        pass
    time.sleep(seconds)
    proc.terminate()
    try:
        out, _ = proc.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, _ = proc.communicate()
    body = header + (out or "(no server output)").splitlines()
    log_path.write_text("\n".join(body), encoding="utf-8")
    return body


def probe_endpoints():
    cmd = [sys.executable, "-m", "http.server", str(PORT), "--directory", str(PUBLIC)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    time.sleep(1)
    rows = [f"=== HTTP probes (port {PORT}) ===", ""]
    for path in ["index.html", "app.html", "style.css", "manifest.json", "app.html?script=dGVzdA=="]:
        url = f"http://127.0.0.1:{PORT}/{path}"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                rows.append(f"GET /{path} -> {resp.status} ({len(resp.read())} bytes)")
        except Exception as e:
            rows.append(f"GET /{path} -> ERROR: {e}")
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
    return rows


def main():
    log1 = SCRATCH / "launch-1.log"
    log2 = SCRATCH / "launch-2.log"
    combined = SCRATCH / "launch.log"

    r1 = capture_server_transcript("RUN 1 server stdout/stderr", log1)
    time.sleep(0.5)
    r2 = capture_server_transcript("RUN 2 server stdout/stderr", log2)
    probe_rows = probe_endpoints()
    (SCRATCH / "launch-probes.log").write_text("\n".join(probe_rows), encoding="utf-8")

    combined.write_text("\n".join(r1 + ["", ""] + r2 + ["", ""] + probe_rows), encoding="utf-8")
    print(combined.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()