#!/usr/bin/env python3
"""
Execute runSpectorCoreTests() from shipped app.html via headless Edge/Chromium.
Writes captured output to scratch dir for verification audit.
"""
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "public" / "app.html"
SCRATCH = Path(r"C:\Users\USER\AppData\Local\Temp\grok-goal-ee54e3f7c3b7\implementer")
SCRATCH.mkdir(parents=True, exist_ok=True)
OUT = SCRATCH / "pure-logic-tests.txt"

EDGE_PATHS = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]


def find_browser():
    for p in EDGE_PATHS:
        if p.is_file():
            return p
    return None


def extract_results(dump_text):
    m = re.search(r'<pre id="spector-test-output">(.*?)</pre>', dump_text, re.DOTALL)
    if not m:
        return None
    raw = html.unescape(m.group(1).strip())
    return json.loads(raw)


def main():
    lines = ["=== SpectorCore execution via headless browser ===", f"Source: {APP}", ""]

    browser = find_browser()
    if not browser:
        lines.append("BROWSER: not found (msedge/chrome unavailable)")
        lines.append("FALLBACK: cannot execute JS; static audit only")
        OUT.write_text("\n".join(lines), encoding="utf-8")
        print("\n".join(lines))
        sys.exit(2)

    lines.append(f"BROWSER: {browser}")

    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8099", "--directory", str(ROOT / "public")],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(1.5)

    url = "http://127.0.0.1:8099/app.html?test"
    lines.append(f"URL: {url}")

    dump_path = SCRATCH / "test-dump.html"
    try:
        proc = subprocess.run(
            [
                str(browser), "--headless=new", "--disable-gpu", "--no-sandbox",
                f"--dump-dom={dump_path}", "--virtual-time-budget=5000",
                "--run-all-compositor-stages-before-draw", url,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        dump = ""
        if dump_path.is_file():
            dump = dump_path.read_text(encoding="utf-8", errors="replace")
        if not dump.strip():
            dump = (proc.stdout or "") + (proc.stderr or "")
        lines.append(f"exit_code: {proc.returncode}")
        lines.append(f"title: {'ALL PASS' if 'SpectorTest: ALL PASS' in dump else 'check dump'}")

        results = extract_results(dump)
        if results:
            lines.append("")
            lines.append(f"[SpectorTest] allPass={results.get('allPass')}")
            for r in results.get("results", []):
                status = "PASS" if r.get("pass") else "FAIL"
                lines.append(f"  [{status}] {r.get('label')}")
            lines.append("")
            lines.append("FULL JSON:")
            lines.append(json.dumps(results, indent=2))
            OUT.write_text("\n".join(lines), encoding="utf-8")
            print("\n".join(lines))
            server.terminate()
            sys.exit(0 if results.get("allPass") else 1)

        lines.append("ERROR: could not parse spector-test-output from browser dump")
        lines.append(f"dump snippet: {dump[:1200]}")
    except Exception as e:
        lines.append(f"ERROR: {e}")
    finally:
        server.terminate()

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    sys.exit(1)


if __name__ == "__main__":
    main()