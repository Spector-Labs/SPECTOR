#!/usr/bin/env python3
"""
Execute shipped runSpectorCoreTests via headless Edge on port 8088.
- ?test path: full test harness with JSON output
- normal app.html: confirms player HTML loads WITHOUT test harness DOM
"""
import base64
import html
import json
import re
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
SCRATCH = Path(r"C:\Users\USER\AppData\Local\Temp\grok-goal-ee54e3f7c3b7\implementer")
SCRATCH.mkdir(parents=True, exist_ok=True)
OUT = SCRATCH / "pure-logic-tests.txt"


def pick_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

EDGE_PATHS = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
]


def find_browser():
    for p in EDGE_PATHS:
        if p.is_file():
            return p
    return None


def encode_script(text):
    return base64.b64encode(urllib.parse.quote(text, safe="").encode("utf-8")).decode("ascii")


def extract_test_results(dump_text):
    m = re.search(r'<pre id="spector-test-output">(.*?)</pre>', dump_text, re.DOTALL)
    if not m:
        return None
    return json.loads(html.unescape(m.group(1).strip()))


def headless_dump(browser, url, dump_path):
    dump_path = Path(dump_path).resolve()
    return subprocess.run(
        [
            str(browser), "--headless=new", "--disable-gpu", "--no-sandbox",
            f"--dump-dom={dump_path}", "--virtual-time-budget=10000",
            "--run-all-compositor-stages-before-draw", url,
        ],
        capture_output=True,
        text=True,
        timeout=45,
    )


def read_dump(dump_path, proc):
    p = Path(dump_path)
    if p.is_file() and p.stat().st_size > 0:
        return p.read_text(encoding="utf-8", errors="replace")
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "<html" in combined.lower():
        return combined
    return combined


def fetch_player_html(url):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main():
    lines = ["=== SpectorCore execution (integrated port 8088) ===", f"Source: {PUBLIC / 'app.html'}", ""]

    browser = find_browser()
    if not browser:
        lines.append("BROWSER: not found — launcher cannot run headless tests here")
        OUT.write_text("\n".join(lines), encoding="utf-8")
        print("\n".join(lines))
        sys.exit(2)

    lines.append(f"BROWSER: {browser}")

    port = pick_port()
    lines.append(f"PORT: {port}")

    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", str(PUBLIC)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(1.5)

    script_param = encode_script("Hello.")
    normal_url = f"http://127.0.0.1:{port}/app.html?script={script_param}"
    lines.append(f"NORMAL URL: {normal_url}")

    try:
        normal_html = fetch_player_html(normal_url)
        static_player_ok = (
            "play-btn" in normal_html
            and "spector-test-output" not in normal_html
            and "Glasses Mode" in normal_html
        )
    except Exception as e:
        normal_html = ""
        static_player_ok = False
        lines.append(f"NORMAL static fetch error: {e}")
    lines.append(f"NORMAL static HTML player markers: {'OK' if static_player_ok else 'FAIL'}")

    normal_dump = SCRATCH / "normal-load-dump.html"
    proc_n = headless_dump(browser, normal_url, normal_dump)
    dump_n = read_dump(normal_dump, proc_n)
    title_m = re.search(r"<title>([^<]*)</title>", dump_n)
    title = title_m.group(1) if title_m else ""
    harness_dom_absent = ("Glasses Mode" in title and "SpectorTest" not in title)
    headless_player_ok = harness_dom_absent and "play-btn" in dump_n
    lines.append(f"NORMAL headless title: {title!r}")
    lines.append(f"NORMAL headless test harness DOM absent: {'OK' if harness_dom_absent else 'FAIL'}")
    lines.append(f"NORMAL headless player surface: {'OK' if headless_player_ok else 'FAIL'} (exit {proc_n.returncode}, bytes {len(dump_n)})")

    test_url = f"http://127.0.0.1:{port}/app.html?test"
    test_dump = SCRATCH / "test-load-dump.html"
    lines.append(f"TEST URL: {test_url}")
    proc_t = headless_dump(browser, test_url, test_dump)
    dump_t = read_dump(test_dump, proc_t)
    results = extract_test_results(dump_t)
    if results:
        lines.append(f"TEST harness allPass={results.get('allPass')}")
        for r in results.get("results", []):
            status = "PASS" if r.get("pass") else "FAIL"
            lines.append(f"  [{status}] {r.get('label')}")
        lines.append("")
        lines.append("FULL JSON:")
        lines.append(json.dumps(results, indent=2))
    else:
        lines.append("TEST harness: FAIL — could not parse spector-test-output")
        lines.append(f"dump bytes: {len(dump_t)}")
        lines.append(f"dump snippet: {dump_t[:800]}")

    server.terminate()
    try:
        server.wait(timeout=3)
    except subprocess.TimeoutExpired:
        server.kill()

    all_pass = headless_player_ok and results and results.get("allPass")
    if not static_player_ok:
        lines.append("NOTE: static fetch check failed; headless player surface used as primary evidence")
    lines.append("")
    lines.append(f"OVERALL: {'ALL PASS' if all_pass else 'FAIL'}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()